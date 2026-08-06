from __future__ import annotations

import base64
import asyncio
import json

import httpx
import pytest

from gateway.app.config import Settings
from gateway.app.tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderCallError, ProviderConfigurationError
from scripts.test_tts_provider import doubao_tts_config_status


def test_doubao_tts_config_reports_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("DOUBAO_TTS_APP_ID", "DOUBAO_TTS_ACCESS_TOKEN", "DOUBAO_TTS_TOKEN", "DOUBAO_TTS_KEY", "DOUBAO_TTS_API_KEY", "DOUBAO_TTS_SPEAKER", "DOUBAO_TTS_VOICE_TYPE"):
        monkeypatch.delenv(key, raising=False)
    settings = Settings(doubao_tts_voice_type="", doubao_tts_speaker="")
    with pytest.raises(ProviderConfigurationError) as exc:
        DoubaoTTSConfig.from_settings(settings)
    assert "DOUBAO_TTS_AUTH" in exc.value.missing
    assert "DOUBAO_TTS_SPEAKER" in exc.value.missing


def test_doubao_tts_config_status_redacts_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAO_TTS_APP_ID", "appid-secret-like")
    monkeypatch.setenv("DOUBAO_TTS_ACCESS_TOKEN", "token-secret-like")
    monkeypatch.setenv("DOUBAO_TTS_SPEAKER", "speaker-secret-like")
    monkeypatch.setenv("DOUBAO_TTS_RESOURCE_ID", "resource-secret-like")

    status = doubao_tts_config_status()

    assert status["ok"] is True
    assert status["required"]["DOUBAO_TTS_APP_ID"] == "configured"
    assert "appid-secret-like" not in str(status)
    assert "token-secret-like" not in str(status)
    assert "speaker-secret-like" not in str(status)
    assert "resource-secret-like" not in str(status)


def test_doubao_tts_provider_builds_v3_stream_payload() -> None:
    asyncio.run(_assert_doubao_tts_provider_builds_v3_stream_payload())


async def _assert_doubao_tts_provider_builds_v3_stream_payload() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["headers"] = dict(request.headers)
        seen["payload"] = request.read().decode("utf-8")
        frame = {"code": 0, "data": base64.b64encode(b"MP3").decode("ascii")}
        end = {"code": 20000000}
        return httpx.Response(
            200,
            content=(json.dumps(frame, separators=(",", ":")) + json.dumps(end, separators=(",", ":"))).encode("utf-8"),
            headers={"content-type": "application/json"},
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    config = DoubaoTTSConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        cluster="volcano_tts",
        speaker="speaker-test",
        resource_id="seed-tts-2.0",
        endpoint="https://openspeech.bytedance.com/api/v3/tts/unidirectional",
        encoding="mp3",
        sample_rate=24000,
        speech_rate=-5,
        uid="unit-test",
        timeout_seconds=3,
    )
    provider = DoubaoTTSProvider(config, client=client)
    result = await provider.synthesize("您好", voice_id=None, request_id="req-tts")
    await client.aclose()

    assert result["content"] == b"MP3"
    assert result["content_type"] == "audio/mpeg"
    assert dict(seen["headers"])["x-api-app-id"] == "appid-test"
    assert dict(seen["headers"])["x-api-access-key"] == "token-test"
    assert dict(seen["headers"])["x-api-resource-id"] == "seed-tts-2.0"
    assert '"speaker":"speaker-test"' in str(seen["payload"])
    assert '"sample_rate":24000' in str(seen["payload"])


def test_doubao_tts_provider_keeps_v1_compatibility() -> None:
    asyncio.run(_assert_doubao_tts_provider_keeps_v1_compatibility())


async def _assert_doubao_tts_provider_keeps_v1_compatibility() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["headers"] = dict(request.headers)
        seen["payload"] = request.read().decode("utf-8")
        return httpx.Response(200, json={"code": 0, "data": base64.b64encode(b"MP3DATA").decode("ascii")})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    config = DoubaoTTSConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        cluster="volcano_tts",
        speaker="voice-test",
        resource_id="seed-tts-2.0",
        endpoint="https://openspeech.bytedance.com/api/v1/tts",
        encoding="mp3",
        sample_rate=24000,
        speech_rate=-5,
        uid="unit-test",
        timeout_seconds=3,
    )
    provider = DoubaoTTSProvider(config, client=client)
    result = await provider.synthesize("您好", voice_id=None, request_id="req-tts")
    await client.aclose()

    assert result["content"] == b"MP3DATA"
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
            api_key=None,
            cluster="bad",
            speaker="bad",
            resource_id="seed-tts-2.0",
            endpoint="https://openspeech.bytedance.com/api/v1/tts",
            encoding="mp3",
            sample_rate=24000,
            speech_rate=-5,
            uid="unit-test",
            timeout_seconds=3,
        ),
        client=client,
    )
    with pytest.raises(ProviderCallError) as exc:
        await provider.synthesize("您好", voice_id=None, request_id="req-tts")
    await client.aclose()
    assert exc.value.code == "TTS_PROVIDER_ERROR"
