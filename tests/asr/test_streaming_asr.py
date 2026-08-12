from __future__ import annotations

import asyncio
import struct

from fastapi.testclient import TestClient

import gateway.app.main as main_module
from gateway.app.streaming_asr import FRAME_BYTES, SPEECH_END_SILENT_FRAMES, WebRtcVadState, pcm_to_wav


app = main_module.app


class SequenceDetector:
    def __init__(self, values: list[bool]) -> None:
        self.values = iter(values)

    def is_speech(self, frame: bytes, sample_rate: int) -> bool:
        assert len(frame) == FRAME_BYTES
        assert sample_rate == 16_000
        return next(self.values)


def test_vad_requires_three_of_five_and_ends_after_three_seconds() -> None:
    detector = SequenceDetector([True, False, True, False, True] + [False] * SPEECH_END_SILENT_FRAMES)
    vad = WebRtcVadState(detector=detector)
    frame = bytes(FRAME_BYTES)

    events = [vad.accept(frame) for _ in range(5)]
    assert events[-1].speech_started is True
    tail = [vad.accept(frame) for _ in range(SPEECH_END_SILENT_FRAMES)]
    assert tail[-1].speech_ended is True


def test_pcm_wav_has_expected_format() -> None:
    wav = pcm_to_wav(bytes(FRAME_BYTES * 2))
    assert wav[:4] == b"RIFF"
    assert wav[8:12] == b"WAVE"


def test_stream_contract_returns_one_final_answer() -> None:
    client = TestClient(app)
    client.post(
        "/api/v1/knowledge/index",
        json={"documents": [{"id": "stream-faq", "title": "服务时间", "text": "服务时间以现场公告为准。", "status": "approved"}]},
    )
    voiced = b"".join(struct.pack("<h", 12_000 if index % 2 == 0 else -12_000) for index in range(320))
    silence = bytes(FRAME_BYTES)
    with client.websocket_connect("/api/v1/dialogue/stream") as websocket:
        websocket.send_json({"type": "start", "request_id": "req-stream-test", "session_id": "sess-stream", "generation": 7})
        ready = websocket.receive_json()
        assert ready["type"] == "ready"
        for _ in range(8):
            websocket.send_bytes(voiced)
        for _ in range(SPEECH_END_SILENT_FRAMES + 10):
            websocket.send_bytes(silence)
        events = []
        while True:
            event = websocket.receive_json()
            events.append(event)
            if event["type"] in {"tts_ready", "error"}:
                break

    types = [event["type"] for event in events]
    assert "speech_started" in types
    assert "partial_transcript" in types
    assert types.count("final_transcript") == 1
    assert types.count("answer") == 1
    assert types[-1] == "tts_ready"
    assert all(event["request_id"] == "req-stream-test" for event in events)
    assert all(event.get("generation", 7) == 7 for event in events)


def test_stream_contract_rejects_non_integer_generation() -> None:
    client = TestClient(app)
    with client.websocket_connect("/api/v1/dialogue/stream") as websocket:
        websocket.send_json(
            {
                "type": "start",
                "request_id": "req-invalid-generation",
                "session_id": "sess-stream",
                "generation": "web-realtime",
            }
        )
        event = websocket.receive_json()

    assert event == {
        "type": "error",
        "request_id": "req-invalid-generation",
        "code": "INVALID_START",
        "message": "invalid stream start event",
    }


def test_stream_contract_keeps_slow_answer_alive(monkeypatch) -> None:
    original_run_dialogue = main_module._run_dialogue

    async def delayed_dialogue(*args, **kwargs):
        await asyncio.sleep(0.04)
        return await original_run_dialogue(*args, **kwargs)

    monkeypatch.setattr(main_module, "_run_dialogue", delayed_dialogue)
    monkeypatch.setattr(main_module, "STREAM_PROGRESS_INTERVAL_SECONDS", 0.01)
    client = TestClient(app)
    voiced = b"".join(struct.pack("<h", 12_000 if index % 2 == 0 else -12_000) for index in range(320))

    with client.websocket_connect("/api/v1/dialogue/stream") as websocket:
        websocket.send_json({"type": "start", "request_id": "req-heartbeat", "session_id": "sess-stream", "generation": 8})
        assert websocket.receive_json()["type"] == "ready"
        for _ in range(8):
            websocket.send_bytes(voiced)
        websocket.send_json({"type": "stop", "request_id": "req-heartbeat"})
        events = []
        while True:
            event = websocket.receive_json()
            events.append(event)
            if event["type"] in {"tts_ready", "error"}:
                break

    assert events[-1]["type"] == "tts_ready"
    assert any(event.get("stage") == "answering" and event.get("heartbeat") is True for event in events)
