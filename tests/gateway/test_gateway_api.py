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

    readiness = client.get("/api/v1/readiness")
    assert readiness.status_code == 200
    readiness_payload = readiness.json()
    assert readiness_payload["ready"] is True
    assert readiness_payload["providers"]["asr"]["provider"] == "mock"

    config = client.get("/api/v1/client/config")
    assert config.status_code == 200
    payload = config.json()
    assert payload["display_mode"] == "idle_video_voice"
    assert "/api/v1/dialogue/audio" == payload["api"]["dialogue_audio"]


def test_local_kiosk_demo_loads_real_presentation_and_dialogue_contracts() -> None:
    response = client.get("/demo/kiosk")
    assert response.status_code == 200
    assert 'id="avatar"' in response.text
    assert "/api/v1/client/bootstrap?width=1080&height=1920&orientation=portrait" in response.text
    assert "manifest.video?.url" in response.text
    assert "manifest.background?.url" in response.text
    assert "navigator.mediaDevices.getUserMedia" in response.text
    assert "SILENCE_AUTO_SEND_MS = 3000" in response.text
    assert "SPEECH_CONFIRMATION_FRAMES = 2" in response.text
    assert "shouldAutoSendAfterSilence" in response.text
    assert "startSilenceMonitoring(microphone)" in response.text
    assert "stopRecording('silence')" in response.text
    assert "stopRecording('manual')" in response.text
    assert "form.append('audio'" in response.text
    assert "/api/v1/dialogue/audio" in response.text
    assert "/api/v1/dialogue/text" in response.text
    assert "/api/v1/audio/" in response.text


def test_client_bootstrap_is_versioned_and_etag_aware() -> None:
    response = client.get("/api/v1/client/bootstrap?width=1080&height=1920&orientation=portrait&version_code=1")
    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == 1
    assert payload["bundle_version"] == response.headers["etag"].strip('"')
    assert payload["config"]["refresh_interval_seconds"] == 60
    assert payload["display_profile"]["orientation"] == "portrait"

    unchanged = client.get(
        "/api/v1/client/bootstrap?width=1080&height=1920&orientation=portrait&version_code=1",
        headers={"If-None-Match": response.headers["etag"]},
    )
    assert unchanged.status_code == 304
    assert unchanged.content == b""


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


def test_gateway_reports_embedding_configuration_stage(monkeypatch) -> None:
    import importlib

    monkeypatch.setenv("JIYANGJIA_EMBEDDING_PROVIDER", "doubao")
    for key in (
        "DOUBAO_EMBEDDING_API_KEY",
        "EMBEDDING_API_KEY",
        "DOUBAO_API_KEY",
        "ARK_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    import gateway.app.main as main_module

    reloaded = importlib.reload(main_module)
    configured_client = TestClient(reloaded.app)

    readiness = configured_client.get("/api/v1/readiness")
    assert readiness.status_code == 200
    readiness_payload = readiness.json()
    assert readiness_payload["ready"] is False
    assert readiness_payload["providers"]["embedding"]["ready"] is False
    assert any("DOUBAO_EMBEDDING_API_KEY" in item for item in readiness_payload["providers"]["embedding"]["missing"])

    response = configured_client.post("/api/v1/knowledge/search", json={"query": "积养家"})
    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["code"] == "BLOCKED_PROVIDER_CREDENTIALS"
    assert detail["failed_stage"] == "embedding_provider_config"

    monkeypatch.setenv("JIYANGJIA_EMBEDDING_PROVIDER", "mock")
    importlib.reload(main_module)
