from __future__ import annotations

import base64
import asyncio

import httpx
import pytest

from gateway.app.config import Settings
from gateway.app.tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderCallError, ProviderConfigurationError
from scripts.test_tts_provider import doubao_tts_config_status


def test_doubao_tts_config_reports_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("DOUBAO_TTS_APP_ID", "DOUBAO_TTS_ACCESS_TOKEN", "DOUBAO_TTS_TOKEN", "DOUBAO_TTS_KEY"):
        monkeypatch.delenv(key, raising=False)
    settings = Settings(doubao_tts_voice_type="")
    with pytest.raises(ProviderConfigurationError) as exc:
        DoubaoTTSConfig.from_settings(settings)
    assert "DOUBAO_TTS_APP_ID" in exc.value.missing
    assert "DOUBAO_TTS_ACCESS_TOKEN" in exc.value.missing
    assert "DOUBAO_TTS_VOICE_TYPE" in exc.value.missing


def test_doubao_tts_config_status_redacts_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAO_TTS_APP_ID", "appid-secret-like")
    monkeypatch.setenv("DOUBAO_TTS_ACCESS_TOKEN", "token-secret-like")
    monkeypatch.setenv("DOUBAO_TTS_VOICE_TYPE", "voice-secret-like")

    status = doubao_tts_config_status()

    assert status["ok"] is True
    assert status["required"]["DOUBAO_TTS_APP_ID"] == "configured"
    assert "appid-secret-like" not in str(status)
    assert "token-secret-like" not in str(status)
    assert "voice-secret-like" not in str(status)


def test_doubao_tts_provider_builds_official_http_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    asyncio.run(_assert_doubao_tts_provider_builds_official_http_payload())


async def _assert_doubao_tts_provider_builds_official_http_payload() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["headers"] = dict(request.headers)
        seen["payload"] = request.read().decode("utf-8")
        return httpx.Response(
            200,
            json={"code": 0, "data": base64.b64encode(b"MP3DATA").decode("ascii")},
            headers={"content-type": "application/json"},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    config = DoubaoTTSConfig(
        app_id="appid-test",
        access_token="token-test",
        cluster="volcano_tts",
        voice_type="voice-test",
        endpoint="https://openspeech.bytedance.com/api/v1/tts",
        encoding="mp3",
        uid="unit-test",
        timeout_seconds=3,
    )
    provider = DoubaoTTSProvider(config, client=client)
    result = await provider.synthesize("您好", voice_id=None, request_id="req-tts")
    await client.aclose()

    assert result["content"] == b"MP3DATA"
    assert result["content_type"] == "audio/mpeg"
    assert "Bearer; token-test" == dict(seen["headers"])["authorization"]
    assert '"appid":"appid-test"' in str(seen["payload"])
    assert '"voice_type":"voice-test"' in str(seen["payload"])
    assert '"operation":"query"' in str(seen["payload"])


def test_doubao_tts_provider_maps_error_response() -> None:
    asyncio.run(_assert_doubao_tts_provider_maps_error_response())


async def _assert_doubao_tts_provider_maps_error_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"code": 3001, "message": "voice_type / cluster error"})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = DoubaoTTSProvider(
        DoubaoTTSConfig(
            app_id="appid-test",
            access_token="token-test",
            cluster="bad",
            voice_type="bad",
            endpoint="https://openspeech.bytedance.com/api/v1/tts",
            encoding="mp3",
            uid="unit-test",
            timeout_seconds=3,
        ),
        client=client,
    )
    with pytest.raises(ProviderCallError) as exc:
        await provider.synthesize("您好", voice_id=None, request_id="req-tts")
    await client.aclose()
    assert exc.value.code == "TTS_PROVIDER_ERROR"
