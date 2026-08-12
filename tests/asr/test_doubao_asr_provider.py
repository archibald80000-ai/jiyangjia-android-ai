from __future__ import annotations

import asyncio
import json

import pytest

from gateway.app.asr import (
    DoubaoASRConfig,
    DoubaoASRProvider,
    FULL_SERVER_RESPONSE,
    JSON_SERIALIZATION,
    NEG_WITH_SEQUENCE,
    build_asr_request,
    build_client_packet,
    parse_server_packet,
)
from gateway.app.config import Settings
from gateway.app.tts import ProviderCallError, ProviderConfigurationError
from scripts.test_asr_provider import doubao_asr_config_status


class FakeWebSocket:
    def __init__(self, frames: list[bytes]) -> None:
        self.frames = frames
        self.sent: list[bytes] = []

    async def __aenter__(self) -> "FakeWebSocket":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def send(self, data: bytes) -> None:
        self.sent.append(data)

    async def recv(self) -> bytes:
        if not self.frames:
            await asyncio.sleep(0.01)
            raise asyncio.TimeoutError
        return self.frames.pop(0)


def test_doubao_asr_config_reports_missing_auth(monkeypatch: pytest.MonkeyPatch) -> None:
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
    with pytest.raises(ProviderConfigurationError) as exc:
        DoubaoASRConfig.from_settings(Settings())
    assert "DOUBAO_ASR_AUTH" in exc.value.missing


def test_doubao_asr_config_status_redacts_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAO_ASR_APP_ID", "appid-secret-like")
    monkeypatch.setenv("DOUBAO_ASR_ACCESS_TOKEN", "token-secret-like")
    monkeypatch.setenv("DOUBAO_ASR_RESOURCE_ID", "resource-secret-like")

    status = doubao_asr_config_status()

    assert status["ok"] is True
    assert status["required"]["DOUBAO_ASR_APP_ID"] == "configured"
    assert "appid-secret-like" not in str(status)
    assert "token-secret-like" not in str(status)
    assert "resource-secret-like" not in str(status)


def test_doubao_asr_packet_round_trip() -> None:
    packet = build_client_packet(
        FULL_SERVER_RESPONSE,
        NEG_WITH_SEQUENCE,
        JSON_SERIALIZATION,
        -1,
        {"result": {"text": "欢迎来到积养家。"}},
    )
    parsed = parse_server_packet(packet)

    assert parsed["is_last_package"] is True
    assert parsed["payload"]["result"]["text"] == "欢迎来到积养家。"


def test_doubao_asr_request_omits_corpus_without_hotword_table() -> None:
    config = DoubaoASRConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        endpoint="wss://example.test",
        resource_id="resource-test",
        audio_format="wav",
        uid="unit-test",
        chunk_bytes=32000,
        timeout_seconds=3,
    )

    assert "corpus" not in build_asr_request(config)


def test_doubao_asr_request_prefers_hotword_table_id() -> None:
    config = DoubaoASRConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        endpoint="wss://example.test",
        resource_id="resource-test",
        audio_format="wav",
        uid="unit-test",
        chunk_bytes=32000,
        timeout_seconds=3,
        boosting_table_id="table-id-test",
        boosting_table_name="table-name-test",
    )

    assert build_asr_request(config)["corpus"] == {"boosting_table_id": "table-id-test"}


def test_doubao_asr_request_serializes_direct_corrections() -> None:
    config = DoubaoASRConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        endpoint="wss://example.test",
        resource_id="resource-test",
        audio_format="wav",
        uid="unit-test",
        chunk_bytes=32000,
        timeout_seconds=3,
        context_json=json.dumps({"correct_words": {"吉养家": "积养家"}}, ensure_ascii=False),
    )

    request = build_asr_request(config)

    assert json.loads(request["context"])["correct_words"]["吉养家"] == "积养家"


def test_doubao_asr_request_rejects_invalid_context_json() -> None:
    config = DoubaoASRConfig(
        app_id="appid-test",
        access_token="token-test",
        api_key=None,
        endpoint="wss://example.test",
        resource_id="resource-test",
        audio_format="wav",
        uid="unit-test",
        chunk_bytes=32000,
        timeout_seconds=3,
        context_json="not-json",
    )

    with pytest.raises(ProviderConfigurationError) as exc:
        build_asr_request(config)
    assert "DOUBAO_ASR_CONTEXT_JSON" in exc.value.missing


def test_doubao_asr_provider_builds_websocket_headers_and_audio_packets() -> None:
    asyncio.run(_assert_doubao_asr_provider_builds_websocket_headers_and_audio_packets())


async def _assert_doubao_asr_provider_builds_websocket_headers_and_audio_packets() -> None:
    final_frame = build_client_packet(
        FULL_SERVER_RESPONSE,
        NEG_WITH_SEQUENCE,
        JSON_SERIALIZATION,
        -1,
        {"result": {"text": "欢迎来到积养家。"}},
    )
    fake = FakeWebSocket([final_frame])
    seen: dict[str, object] = {}

    async def connect(endpoint: str, headers: dict[str, str], max_size: int) -> FakeWebSocket:
        seen["endpoint"] = endpoint
        seen["headers"] = headers
        seen["max_size"] = max_size
        return fake

    provider = DoubaoASRProvider(
        DoubaoASRConfig(
            app_id="appid-test",
            access_token="token-test",
            api_key=None,
            endpoint="wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_nostream",
            resource_id="volc.bigasr.sauc.duration",
            audio_format="wav",
            uid="unit-test",
            chunk_bytes=4,
            timeout_seconds=3,
        ),
        connect=connect,
    )
    result = await provider.transcribe(b"12345678", "audio/wav", "req-asr")

    assert result["text"] == "欢迎来到积养家。"
    assert result["provider"] == "doubao"
    assert seen["headers"]["X-Api-App-Key"] == "appid-test"
    assert seen["headers"]["X-Api-Access-Key"] == "token-test"
    assert seen["headers"]["X-Api-Resource-Id"] == "volc.bigasr.sauc.duration"
    assert len(fake.sent) == 2


def test_doubao_asr_provider_rejects_empty_audio() -> None:
    provider = DoubaoASRProvider(
        DoubaoASRConfig(
            app_id="appid-test",
            access_token="token-test",
            api_key=None,
            endpoint="wss://example.test",
            resource_id="volc.bigasr.sauc.duration",
            audio_format="wav",
            uid="unit-test",
            chunk_bytes=32000,
            timeout_seconds=3,
        )
    )

    with pytest.raises(ProviderCallError) as exc:
        asyncio.run(provider.transcribe(b"", "audio/wav", "req-empty"))
    assert exc.value.code == "EMPTY_AUDIO"


def test_doubao_asr_provider_maps_timeout() -> None:
    asyncio.run(_assert_doubao_asr_provider_maps_timeout())


async def _assert_doubao_asr_provider_maps_timeout() -> None:
    fake = FakeWebSocket([])

    async def connect(endpoint: str, headers: dict[str, str], max_size: int) -> FakeWebSocket:
        return fake

    provider = DoubaoASRProvider(
        DoubaoASRConfig(
            app_id="appid-test",
            access_token="token-test",
            api_key=None,
            endpoint="wss://example.test",
            resource_id="volc.bigasr.sauc.duration",
            audio_format="wav",
            uid="unit-test",
            chunk_bytes=32000,
            timeout_seconds=0.02,
        ),
        connect=connect,
    )

    with pytest.raises(ProviderCallError) as exc:
        await provider.transcribe(b"RIFFMOCK", "audio/wav", "req-timeout")
    assert exc.value.code == "ASR_TIMEOUT"
