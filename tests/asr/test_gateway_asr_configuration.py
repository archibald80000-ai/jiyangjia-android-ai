from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


def test_gateway_reports_missing_doubao_asr_credentials(monkeypatch) -> None:
    monkeypatch.setenv("JIYANGJIA_ASR_PROVIDER", "doubao")
    for key in (
        "DOUBAO_ASR_APP_ID",
        "DOUBAO_ASR_ACCESS_TOKEN",
        "DOUBAO_ASR_TOKEN",
        "DOUBAO_ASR_KEY",
        "DOUBAO_ASR_API_KEY",
        "DOUBAO_REALTIME_APP_ID",
        "DOUBAO_REALTIME_ACCESS_TOKEN",
    ):
        monkeypatch.delenv(key, raising=False)

    import gateway.app.main as main_module

    reloaded = importlib.reload(main_module)
    client = TestClient(reloaded.app)
    response = client.post(
        "/api/v1/dialogue/audio",
        files={"audio": ("question.wav", b"RIFFMOCK", "audio/wav")},
        data={"session_id": "sess-audio"},
    )

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["code"] == "BLOCKED_PROVIDER_CREDENTIALS"
    assert "DOUBAO_ASR_AUTH" in detail["missing"]

    monkeypatch.setenv("JIYANGJIA_ASR_PROVIDER", "mock")
    importlib.reload(main_module)
