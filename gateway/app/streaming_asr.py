from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any

import webrtcvad

from .asr import (
    AUDIO_ONLY_REQUEST,
    FULL_CLIENT_REQUEST,
    JSON_SERIALIZATION,
    NEG_WITH_SEQUENCE,
    NO_SERIALIZATION,
    POS_SEQUENCE,
    DoubaoASRProvider,
    _extract_text,
    _websocket_connect,
    build_client_packet,
    parse_server_packet,
)
from .tts import ProviderCallError


FRAME_BYTES = 640
SAMPLE_RATE = 16_000
MAX_PCM_BYTES = 1_048_576


@dataclass(frozen=True)
class VadEvent:
    speech_started: bool = False
    speech_ended: bool = False
    no_speech_timeout: bool = False
    max_duration: bool = False


class WebRtcVadState:
    """20 ms WebRTC VAD with bounded start/end hysteresis."""

    def __init__(self, mode: int = 2, detector: Any | None = None) -> None:
        self.detector = detector or webrtcvad.Vad(mode)
        self.window: deque[bool] = deque(maxlen=5)
        self.started = False
        self.silent_frames = 0
        self.total_frames = 0

    def accept(self, frame: bytes) -> VadEvent:
        if len(frame) != FRAME_BYTES:
            raise ValueError(f"PCM frame must be exactly {FRAME_BYTES} bytes")
        self.total_frames += 1
        voiced = bool(self.detector.is_speech(frame, SAMPLE_RATE))
        self.window.append(voiced)
        if not self.started:
            if len(self.window) == 5 and sum(self.window) >= 3:
                self.started = True
                self.silent_frames = 0
                return VadEvent(speech_started=True)
            return VadEvent(no_speech_timeout=self.total_frames >= 400)
        self.silent_frames = 0 if voiced else self.silent_frames + 1
        return VadEvent(
            speech_ended=self.silent_frames >= 40,
            max_duration=self.total_frames >= 1500,
        )


class MockStreamingASRSession:
    def __init__(self) -> None:
        self.frames = 0

    async def push(self, pcm_frame: bytes) -> list[str]:
        self.frames += 1
        return ["模拟语音"] if self.frames == 5 else []

    async def finish(self) -> dict[str, object]:
        return {"text": "积养家模拟语音问题", "provider": "mock", "language": "zh-CN", "confidence": 1.0}

    async def close(self) -> None:
        return None


class MockStreamingASRProvider:
    name = "mock"

    async def open_stream(self, request_id: str) -> MockStreamingASRSession:
        return MockStreamingASRSession()


class DoubaoStreamingASRProvider:
    name = "doubao"

    def __init__(self, provider: DoubaoASRProvider, endpoint: str) -> None:
        self.provider = provider
        self.endpoint = endpoint

    async def open_stream(self, request_id: str) -> "DoubaoStreamingASRSession":
        session = DoubaoStreamingASRSession(self.provider, self.endpoint, request_id)
        await session.open()
        return session


class DoubaoStreamingASRSession:
    def __init__(self, provider: DoubaoASRProvider, endpoint: str, request_id: str) -> None:
        self.provider = provider
        self.endpoint = endpoint
        self.request_id = request_id
        self.connection: Any | None = None
        self.websocket: Any | None = None
        self.sequence = 2
        self.pending: bytes | None = None
        self.latest: dict[str, Any] = {}
        self.last_partial = ""

    async def open(self) -> None:
        connect = self.provider._connect or _websocket_connect
        self.connection = await connect(
            self.endpoint,
            headers=self.provider._headers(self.request_id),
            max_size=100_000_000,
        )
        self.websocket = await self.connection.__aenter__()
        payload = {
            "user": {"uid": self.provider.config.uid},
            "audio": {"format": "pcm", "codec": "raw", "rate": SAMPLE_RATE, "bits": 16, "channel": 1},
            "request": {"model_name": "bigmodel", "enable_itn": True, "enable_punc": True, "enable_ddc": True},
        }
        await self.websocket.send(build_client_packet(FULL_CLIENT_REQUEST, POS_SEQUENCE, JSON_SERIALIZATION, 1, payload))

    async def push(self, pcm_frame: bytes) -> list[str]:
        if len(pcm_frame) != FRAME_BYTES:
            raise ValueError(f"PCM frame must be exactly {FRAME_BYTES} bytes")
        partials: list[str] = []
        if self.pending is not None:
            await self.websocket.send(
                build_client_packet(AUDIO_ONLY_REQUEST, POS_SEQUENCE, NO_SERIALIZATION, self.sequence, self.pending)
            )
            self.sequence += 1
            partials.extend(await self._drain())
        self.pending = pcm_frame
        return partials

    async def finish(self) -> dict[str, object]:
        if self.pending is None:
            raise ProviderCallError("EMPTY_AUDIO", "stream contained no PCM", retryable=False)
        await self.websocket.send(
            build_client_packet(AUDIO_ONLY_REQUEST, NEG_WITH_SEQUENCE, NO_SERIALIZATION, -self.sequence, self.pending)
        )
        while True:
            parsed = parse_server_packet(await self.websocket.recv())
            payload = parsed.get("payload")
            if isinstance(payload, dict):
                self.latest = payload
            if parsed.get("is_last_package"):
                text = _extract_text(self.latest)
                if text:
                    return {"text": text, "provider": "doubao", "language": "zh-CN", "confidence": None}

    async def _drain(self) -> list[str]:
        import asyncio

        partials: list[str] = []
        while True:
            try:
                frame = await asyncio.wait_for(self.websocket.recv(), timeout=0.001)
            except asyncio.TimeoutError:
                break
            parsed = parse_server_packet(frame)
            payload = parsed.get("payload")
            if isinstance(payload, dict):
                self.latest = payload
                text = _extract_text(payload)
                if text and text != self.last_partial:
                    self.last_partial = text
                    partials.append(text)
        return partials

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.__aexit__(None, None, None)
            self.connection = None
            self.websocket = None


def pcm_to_wav(pcm: bytes) -> bytes:
    import io
    import wave

    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm)
    return output.getvalue()
