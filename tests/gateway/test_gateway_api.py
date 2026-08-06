from __future__ import annotations

from fastapi.testclient import TestClient

from gateway.app.main import app
from gateway.app.main import _normalize_transcript_payload


client = TestClient(app)


def index_service_time_doc(doc_id: str = "faq-001") -> None:
    response = client.post(
        "/api/v1/knowledge/index",
        json={
            "documents": [
                {
                    "id": doc_id,
                    "title": "服务时间",
                    "text": "门店服务时间请以当天现场公告为准。",
                    "status": "approved",
                    "source_uri": f"manual://{doc_id}",
                }
            ]
        },
    )
    assert response.status_code == 200


def test_health_and_client_config_include_required_fields() -> None:
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True
    assert health.headers["X-Request-Id"]

    config = client.get("/api/v1/client/config")
    assert config.status_code == 200
    payload = config.json()
    assert payload["display_mode"] == "idle_video_voice"
    assert "/api/v1/dialogue/audio" == payload["api"]["dialogue_audio"]


def test_knowledge_index_search_status_uses_approved_sources() -> None:
    index_service_time_doc("faq-001")
    indexed = client.post(
        "/api/v1/knowledge/index",
        json={
            "documents": [
                {
                    "id": "faq-001",
                    "title": "服务时间",
                    "text": "门店服务时间请以当天现场公告为准。",
                    "status": "approved",
                    "source_uri": "manual://faq-001",
                },
                {
                    "id": "faq-002",
                    "title": "内部价格",
                    "text": "未确认价格不能对外回答。",
                    "status": "draft",
                    "source_uri": "manual://faq-002",
                },
            ]
        },
    )
    assert indexed.status_code == 200
    assert indexed.json()["indexed"] == 2

    search = client.post("/api/v1/knowledge/search", json={"query": "服务时间", "top_k": 3})
    assert search.status_code == 200
    payload = search.json()
    assert payload["status"] == "matched"
    assert payload["matches"][0]["id"] == "faq-001"
    assert payload["sources"][0]["uri"] == "manual://faq-001"

    status = client.get("/api/v1/knowledge/status")
    assert status.status_code == 200
    assert status.json()["documents"]["approved"] >= 1


def test_dialogue_text_returns_request_id_sources_and_audio_id() -> None:
    index_service_time_doc("faq-dialogue")
    response = client.post(
        "/api/v1/dialogue/text",
        headers={"X-Request-Id": "req-test-text"},
        json={"session_id": "sess-test", "text": "服务时间是什么？"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["request_id"] == "req-test-text"
    assert payload["session_id"] == "sess-test"
    assert payload["answer"]["text"]
    assert payload["tts"]["audio_id"].startswith("aud_")

    audio = client.get(f"/api/v1/audio/{payload['tts']['audio_id']}")
    assert audio.status_code == 200
    assert audio.content == b"MOCK_TTS_AUDIO"


def test_dialogue_audio_accepts_supported_upload_and_rejects_bad_type() -> None:
    ok = client.post(
        "/api/v1/dialogue/audio",
        files={"audio": ("question.wav", b"RIFFMOCK", "audio/wav")},
        data={"session_id": "sess-audio", "duration_ms": "300", "sample_rate": "16000", "input_device": "usb"},
    )
    assert ok.status_code == 200
    assert ok.json()["transcript"]["provider"] == "mock"

    bad = client.post(
        "/api/v1/dialogue/audio",
        files={"audio": ("question.bin", b"raw", "application/octet-stream")},
        data={"session_id": "sess-audio"},
    )
    assert bad.status_code == 422
    assert bad.json()["detail"]["code"] == "UNSUPPORTED_AUDIO"


def test_transcript_payload_preserves_raw_text_when_brand_is_normalized() -> None:
    transcript = {
        "text": "您好，欢迎来到季养家。",
        "provider": "doubao",
        "language": "zh-CN",
        "confidence": None,
    }

    normalized = _normalize_transcript_payload(transcript)

    assert normalized["text"] == "您好，欢迎来到积养家。"
    assert normalized["raw_text"] == "您好，欢迎来到季养家。"
    assert normalized["normalization"]["changed"] is True
