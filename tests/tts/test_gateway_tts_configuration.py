from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


def test_gateway_reports_missing_doubao_tts_credentials(monkeypatch) -> None:
    monkeypatch.setenv("JIYANGJIA_TTS_PROVIDER", "doubao")
    for key in (
        "DOUBAO_TTS_APP_ID",
        "DOUBAO_TTS_ACCESS_TOKEN",
        "DOUBAO_TTS_TOKEN",
        "DOUBAO_TTS_KEY",
        "DOUBAO_TTS_API_KEY",
        "DOUBAO_TTS_SPEAKER",
        "DOUBAO_TTS_VOICE_TYPE",
    ):
        monkeypatch.delenv(key, raising=False)

    import gateway.app.main as main_module

    reloaded = importlib.reload(main_module)
    client = TestClient(reloaded.app)
    response = client.post("/api/v1/dialogue/text", json={"text": "服务时间是什么？"})

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["code"] == "BLOCKED_PROVIDER_CREDENTIALS"
    assert "DOUBAO_TTS_AUTH" in detail["missing"]
    assert "DOUBAO_TTS_SPEAKER" in detail["missing"]

    monkeypatch.setenv("JIYANGJIA_TTS_PROVIDER", "mock")
    importlib.reload(main_module)
