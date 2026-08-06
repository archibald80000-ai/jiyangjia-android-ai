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
    assert "DEEPSEEK_API_KEY" in detail["missing"]

    monkeypatch.setenv("JIYANGJIA_LLM_PROVIDER", "mock")
    importlib.reload(main_module)
