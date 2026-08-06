from __future__ import annotations

import json
import time
from pathlib import Path

from fastapi.testclient import TestClient

from gateway.app.main import app


client = TestClient(app)


def _index_e2e_doc() -> None:
    response = client.post(
        "/api/v1/knowledge/index",
        json={
            "documents": [
                {
                    "id": "task013-e2e-mock-question",
                    "title": "TASK-013 Mock 语音咨询",
                    "text": "模拟语音问题的已确认回答：欢迎咨询积养家，工作人员可以继续协助。",
                    "status": "approved",
                    "source_uri": "manual://task013/e2e-mock-question",
                }
            ]
        },
    )
    assert response.status_code == 200


def _fake_wav() -> bytes:
    return b"RIFF\x2c\x00\x00\x00WAVEfmt " + (b"\x00" * 32)


def test_mock_audio_dialogue_loop_returns_request_id_sources_audio_and_subtitles() -> None:
    _index_e2e_doc()
    request_id = "task013-single-cycle"

    response = client.post(
        "/api/v1/dialogue/audio",
        headers={"X-Request-Id": request_id},
        files={"audio": ("question.wav", _fake_wav(), "audio/wav")},
        data={
            "session_id": "sess-task013",
            "request_id": request_id,
            "duration_ms": "300",
            "sample_rate": "16000",
            "input_device": "android-kiosk",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["request_id"] == request_id
    assert payload["session_id"] == "sess-task013"
    assert payload["transcript"]["text"] == "模拟语音问题"
    assert payload["knowledge"]["status"] == "matched"
    assert payload["sources"][0]["uri"] == "manual://task013/e2e-mock-question"
    assert payload["answer"]["subtitles"]

    audio = client.get(f"/api/v1/audio/{payload['tts']['audio_id']}", headers={"X-Request-Id": request_id})
    assert audio.status_code == 200
    assert audio.headers["X-Request-Id"] == request_id
    assert audio.content == b"MOCK_TTS_AUDIO"


def test_thirty_controlled_mock_audio_cycles_write_latency_report() -> None:
    _index_e2e_doc()
    cycle_results: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []

    for index in range(30):
        request_id = f"task013-cycle-{index + 1:02d}"
        started = time.perf_counter()
        response = client.post(
            "/api/v1/dialogue/audio",
            headers={"X-Request-Id": request_id},
            files={"audio": ("question.wav", _fake_wav(), "audio/wav")},
            data={
                "session_id": "sess-task013-30",
                "request_id": request_id,
                "duration_ms": "300",
                "sample_rate": "16000",
                "input_device": "android-kiosk",
            },
        )
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        ok = False
        audio_status = None
        source_count = 0
        try:
            payload = response.json()
            source_count = len(payload.get("sources", []))
            if response.status_code == 200:
                audio = client.get(f"/api/v1/audio/{payload['tts']['audio_id']}", headers={"X-Request-Id": request_id})
                audio_status = audio.status_code
                ok = payload["request_id"] == request_id and audio.status_code == 200 and source_count > 0
        except Exception as exc:  # pragma: no cover - only recorded as evidence on failure
            failures.append({"request_id": request_id, "error": str(exc)})
        if not ok:
            failures.append({"request_id": request_id, "status_code": response.status_code, "audio_status": audio_status})
        cycle_results.append(
            {
                "request_id": request_id,
                "status_code": response.status_code,
                "audio_status": audio_status,
                "latency_ms": elapsed_ms,
                "source_count": source_count,
                "ok": ok,
            }
        )

    latencies = [float(item["latency_ms"]) for item in cycle_results]
    report = {
        "task": "TASK-013",
        "mode": "mock_gateway_audio_dialogue",
        "cycles": len(cycle_results),
        "passed": sum(1 for item in cycle_results if item["ok"]),
        "failed": len(failures),
        "fallback_count": sum(1 for item in cycle_results if item["source_count"] == 0),
        "latency_ms": {
            "min": min(latencies),
            "max": max(latencies),
            "avg": round(sum(latencies) / len(latencies), 2),
        },
        "failures": failures,
        "cycles_detail": cycle_results,
    }
    output_path = Path("docs/evidence/TASK-013/task013-30cycle-pytest-report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    assert report["cycles"] == 30
    assert report["passed"] == 30
    assert report["failed"] == 0
    assert report["fallback_count"] == 0


def test_audio_endpoint_maps_unsupported_upload_as_recoverable_service_error() -> None:
    response = client.post(
        "/api/v1/dialogue/audio",
        headers={"X-Request-Id": "task013-bad-audio"},
        files={"audio": ("question.bin", b"not-audio", "application/octet-stream")},
        data={"session_id": "sess-task013-error"},
    )

    assert response.status_code == 422
    assert response.headers["X-Request-Id"] == "task013-bad-audio"
    assert response.json()["detail"]["message_for_user"] == "当前录音格式不支持，请重试。"
