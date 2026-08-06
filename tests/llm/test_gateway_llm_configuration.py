from __future__ import annotations

import importlib

from fastapi.testclient import TestClient


def test_gateway_reports_missing_deepseek_llm_credentials(monkeypatch) -> None:
    monkeypatch.setenv("JIYANGJIA_LLM_PROVIDER", "deepseek")
    monkeypatch.setenv("JIYANGJIA_TTS_PROVIDER", "mock")
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    import gateway.app.main as main_module

    reloaded = importlib.reload(main_module)
    client = TestClient(reloaded.app)
    response = client.post(
        "/api/v1/dialogue/text",
        json={"session_id": "sess-llm", "text": "服务时间是什么？"},
    )

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["code"] == "BLOCKED_PROVIDER_CREDENTIALS"
    assert detail["failed_stage"] == "llm_provider_config"
    assert "DEEPSEEK_API_KEY" in detail["missing"]

    readiness = client.get("/api/v1/readiness")
    assert readiness.status_code == 200
    readiness_payload = readiness.json()
    assert readiness_payload["ready"] is False
    assert readiness_payload["providers"]["llm"]["ready"] is False
    assert "DEEPSEEK_API_KEY" in readiness_payload["providers"]["llm"]["missing"]

    monkeypatch.setenv("JIYANGJIA_LLM_PROVIDER", "mock")
    importlib.reload(main_module)
