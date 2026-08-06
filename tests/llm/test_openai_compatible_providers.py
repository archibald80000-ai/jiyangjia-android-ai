from __future__ import annotations

import asyncio
import json

import httpx
import pytest

from gateway.app.config import Settings
from gateway.app.llm import (
    OpenAICompatibleChatConfig,
    OpenAICompatibleEmbeddingConfig,
    OpenAICompatibleEmbeddingProvider,
    OpenAICompatibleLLMProvider,
    _endpoint,
)
from gateway.app.tts import ProviderCallError, ProviderConfigurationError
from scripts.test_embedding_provider import embedding_config_status
from scripts.test_llm_provider import llm_config_status


def test_deepseek_config_reports_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)

    with pytest.raises(ProviderConfigurationError) as exc:
        OpenAICompatibleChatConfig.from_settings(Settings(), "deepseek")

    assert exc.value.missing == ["DEEPSEEK_API_KEY"]


def test_llm_config_status_redacts_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-deepseek-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-chat")

    status = llm_config_status("deepseek")

    assert status["ok"] is True
    assert status["required"]["DEEPSEEK_API_KEY"] == "configured"
    assert "secret-deepseek-key" not in str(status)


def test_llm_provider_builds_openai_compatible_chat_payload() -> None:
    asyncio.run(_assert_llm_provider_builds_openai_compatible_chat_payload())


async def _assert_llm_provider_builds_openai_compatible_chat_payload() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["headers"] = dict(request.headers)
        seen["payload"] = json.loads(request.read().decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "model": "deepseek-chat",
                "choices": [{"message": {"role": "assistant", "content": "请咨询现场工作人员。"}}],
                "usage": {"total_tokens": 12},
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleLLMProvider(
        OpenAICompatibleChatConfig(
            provider="deepseek",
            api_key="unit-secret",
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            timeout_seconds=3,
            max_tokens=100,
            temperature=0.1,
        ),
        client=client,
    )

    result = await provider.chat([{"role": "user", "content": "服务时间？"}], [{"title": "服务时间", "excerpt": "门店服务时间以现场公告为准。"}], "req-llm")
    await client.aclose()

    assert seen["url"] == "https://api.deepseek.com/chat/completions"
    assert dict(seen["headers"])["authorization"] == "Bearer unit-secret"
    assert dict(seen["headers"])["x-request-id"] == "req-llm"
    assert dict(seen["payload"])["stream"] is False
    assert dict(seen["payload"])["temperature"] == 0.1
    assert dict(seen["payload"])["messages"][0]["role"] == "system"
    assert "服务时间" in str(seen["payload"])
    assert result["text"] == "请咨询现场工作人员。"
    assert result["source"] == "knowledge_grounded"
    assert result["usage"] == {"total_tokens": 12}


def test_embedding_config_status_redacts_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAO_API_KEY", "secret-ark-key")
    monkeypatch.setenv("DOUBAO_BASE_URL", "https://ark.example.invalid/api/v3")
    monkeypatch.setenv("DOUBAO_EMBEDDING_MODEL", "doubao-embedding-text-test")

    status = embedding_config_status("doubao")

    assert status["ok"] is True
    assert "secret-ark-key" not in str(status)


def test_embedding_provider_builds_openai_compatible_payload() -> None:
    asyncio.run(_assert_embedding_provider_builds_openai_compatible_payload())


async def _assert_embedding_provider_builds_openai_compatible_payload() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["headers"] = dict(request.headers)
        seen["payload"] = json.loads(request.read().decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "model": "doubao-embedding-text-test",
                "data": [{"object": "embedding", "index": 0, "embedding": [0.1, -0.2, 0.3]}],
                "usage": {"total_tokens": 4},
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleEmbeddingProvider(
        OpenAICompatibleEmbeddingConfig(
            provider="doubao",
            api_key="unit-secret",
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            model="doubao-embedding-text-test",
            timeout_seconds=3,
        ),
        client=client,
    )

    result = await provider.embed(["积养家门店"], "req-embedding")
    await client.aclose()

    assert seen["url"] == "https://ark.cn-beijing.volces.com/api/v3/embeddings"
    assert dict(seen["headers"])["authorization"] == "Bearer unit-secret"
    assert dict(seen["payload"])["input"] == ["积养家门店"]
    assert result["vectors"] == [[0.1, -0.2, 0.3]]
    assert result["dimensions"] == 3
    assert result["usage"] == {"total_tokens": 4}


def test_llm_provider_maps_http_rejection() -> None:
    asyncio.run(_assert_llm_provider_maps_http_rejection())


async def _assert_llm_provider_maps_http_rejection() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": {"message": "bad key"}})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleLLMProvider(
        OpenAICompatibleChatConfig(
            provider="deepseek",
            api_key="bad-secret",
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            timeout_seconds=3,
            max_tokens=100,
            temperature=0.2,
        ),
        client=client,
    )
    with pytest.raises(ProviderCallError) as exc:
        await provider.chat([{"role": "user", "content": "测试"}], [], "req-bad")
    await client.aclose()

    assert exc.value.code == "LLM_PROVIDER_REJECTED"
    assert exc.value.retryable is False


def test_endpoint_normalizes_full_openai_compatible_routes() -> None:
    assert _endpoint("https://example.invalid/api/v3/chat/completions", "embeddings") == "https://example.invalid/api/v3/embeddings"
    assert _endpoint("https://example.invalid/api/v3/embeddings", "chat/completions") == "https://example.invalid/api/v3/chat/completions"
