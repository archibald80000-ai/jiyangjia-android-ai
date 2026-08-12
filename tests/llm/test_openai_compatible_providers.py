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
    _embedding_input,
    _embedding_route,
    _endpoint,
    _build_grounded_messages,
    _sanitize_grounded_answer,
    _split_subtitles,
)
from gateway.app.providers import MockLLMProvider
from gateway.app.persona import PERSONA_VERSION, format_approved_context, prepare_spoken_messages, response_direction, response_mode
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


def test_story_mode_applies_a_hard_generation_budget() -> None:
    asyncio.run(_assert_story_mode_applies_a_hard_generation_budget())


async def _assert_story_mode_applies_a_hard_generation_budget() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.update(json.loads(request.read().decode("utf-8")))
        return httpx.Response(200, json={"choices": [{"message": {"content": "这是已确认的小故事。"}}]})

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleLLMProvider(
        OpenAICompatibleChatConfig("doubao", "secret", "https://example.invalid/v1", "model", 3, 300, 0.45),
        client=client,
    )
    result = await provider.chat(
        [{"role": "user", "content": "详细讲讲大有谷的故事。"}],
        [{"title": "大有谷", "excerpt": "已确认资料。"}],
        "req-story-budget",
    )
    await client.aclose()

    assert seen["max_tokens"] == 180
    assert seen["thinking"] == {"type": "disabled"}
    assert result["response_mode"] == "story"


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
    assert result["persona"] == PERSONA_VERSION
    assert result["response_mode"] == "concise"
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


def test_no_context_prompt_refuses_only_unverified_jiyangjia_facts() -> None:
    business = _build_grounded_messages([{"role": "user", "content": "积养家有榴莲吗？"}], [])
    general = _build_grounded_messages([{"role": "user", "content": "帮我写个请假条。"}], [])

    assert "必须明确说明无法确认" in business[1]["content"]
    assert "不要无故拒绝" in general[1]["content"]
    assert "当前不使用品牌知识库" in general[1]["content"]


def test_grounding_prompt_requires_attributed_non_promissory_health_language() -> None:
    messages = _build_grounded_messages(
        [{"role": "user", "content": "生姜有什么特点？"}],
        [{"title": "生姜", "excerpt": "原资料中的传统食养描述。"}],
    )

    assert "传统食养说法" in messages[0]["content"]
    assert "不得扩写成确定疗效" in messages[0]["content"]
    assert "不得使用‘管用’" in messages[0]["content"]


def test_persona_prompt_is_warm_varied_and_still_grounded() -> None:
    messages = _build_grounded_messages(
        [{"role": "user", "content": "详细讲讲七膳鸡汤的故事。"}],
        [{"title": "七膳鸡汤", "excerpt": "这是一段已确认的产品故事。", "source": {"uri": "public://story"}}],
    )

    assert "邻里生活向导" in messages[0]["content"]
    assert "不要每次都使用同一个开场" in messages[0]["content"]
    assert "绝不能增加资料之外的事实" in messages[0]["content"]
    assert "来历介绍" in messages[1]["content"]
    assert "唯一可使用的品牌事实" in messages[2]["content"]
    assert "这是一段已确认的产品故事" in messages[2]["content"]


def test_response_modes_choose_the_right_conversation_rhythm() -> None:
    assert response_mode("讲讲这款汤的来历") == "story"
    assert response_mode("送老人怎么选？") == "choice"
    assert response_mode("门店在哪里？") == "concise"
    assert "90 到 140" in response_direction("详细讲讲它的故事")
    assert "80 到 180" in response_direction("哪一种适合我")
    prepared = prepare_spoken_messages([{"role": "user", "content": "详细讲讲大有谷的故事。"}])
    assert prepared[-1]["content"] == "请用90到140个汉字介绍大有谷的来历，并讲一个已确认资料中的真实细节。"


def test_context_formatter_uses_four_traceable_sources_and_bounded_text() -> None:
    context = [
        {"title": f"资料{i}", "excerpt": "甲" * 1000, "source": {"uri": f"public://{i}"}}
        for i in range(1, 6)
    ]
    rendered = format_approved_context(context)

    assert "[资料4]" in rendered
    assert "[资料5]" not in rendered
    assert "public://1" in rendered
    assert "甲" * 701 not in rendered


def test_subtitles_prefer_natural_chinese_pauses() -> None:
    text = "这是第一句，带有一个自然停顿，也有更长的说明。" + "这是第二句。" * 8
    subtitles = _split_subtitles(text, max_chars=30)

    assert all(len(item) <= 30 for item in subtitles)
    assert "".join(subtitles) == text
    assert subtitles[0].endswith(("，", "。"))


def test_grounded_answer_sanitizer_removes_dynamic_inventory_and_medical_promises() -> None:
    raw = "这款产品不错。\n门店现在有现货，还能现场看。它保证疗效，能治好失眠。欢迎了解。"
    answer = _sanitize_grounded_answer(raw)

    assert "现货" not in answer
    assert "保证疗效" not in answer
    assert "能治好" not in answer
    assert "具体库存和到店情况请咨询现场工作人员" in answer
    assert "不能替代专业诊断或治疗" in answer
    assert "\n" not in answer
    assert "。 " not in answer


def test_mock_llm_routes_general_and_unverified_business_questions() -> None:
    asyncio.run(_assert_mock_llm_routes_general_and_unverified_business_questions())


async def _assert_mock_llm_routes_general_and_unverified_business_questions() -> None:
    provider = MockLLMProvider()
    business = await provider.chat([{"role": "user", "content": "积养家有榴莲吗？"}], [], "req-business")
    general = await provider.chat([{"role": "user", "content": "今天天气怎么样？"}], [], "req-general")

    assert business["source"] == "in_domain_unverified"
    assert "不能确认" in business["text"]
    assert general["source"] == "general_answer_mock"
    assert "通用问题" in general["text"]


def test_endpoint_normalizes_full_openai_compatible_routes() -> None:
    assert _endpoint("https://example.invalid/api/v3/chat/completions", "embeddings") == "https://example.invalid/api/v3/embeddings"
    assert _endpoint("https://example.invalid/api/v3/embeddings", "chat/completions") == "https://example.invalid/api/v3/chat/completions"


def test_multimodal_embedding_model_uses_multimodal_route_and_text_parts() -> None:
    assert _embedding_route("doubao-embedding-vision-241215") == "embeddings/multimodal"
    assert _embedding_input("doubao-embedding-vision-241215", ["积养家"]) == [{"type": "text", "text": "积养家"}]


def test_multimodal_embedding_provider_accepts_nested_single_vector() -> None:
    asyncio.run(_assert_multimodal_embedding_provider_accepts_nested_single_vector())


async def _assert_multimodal_embedding_provider_accepts_nested_single_vector() -> None:
    seen: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["payload"] = json.loads(request.read().decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "model": "doubao-embedding-vision-test",
                "data": [{"index": 0, "object": "embedding", "embedding": [[0.4, 0.5]]}],
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleEmbeddingProvider(
        OpenAICompatibleEmbeddingConfig(
            provider="doubao",
            api_key="unit-secret",
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            model="doubao-embedding-vision-test",
            timeout_seconds=3,
        ),
        client=client,
    )

    result = await provider.embed(["积养家"], "req-mm")
    await client.aclose()

    assert seen["url"] == "https://ark.cn-beijing.volces.com/api/v3/embeddings/multimodal"
    assert dict(seen["payload"])["input"] == [{"type": "text", "text": "积养家"}]
    assert result["vectors"] == [[0.4, 0.5]]
    assert result["dimensions"] == 2


def test_multimodal_embedding_provider_batches_as_single_text_calls() -> None:
    asyncio.run(_assert_multimodal_embedding_provider_batches_as_single_text_calls())


async def _assert_multimodal_embedding_provider_batches_as_single_text_calls() -> None:
    payloads: list[dict[str, object]] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read().decode("utf-8"))
        payloads.append(payload)
        text = payload["input"][0]["text"]
        vector = [1.0, 0.0] if "服务" in text else [0.0, 1.0]
        return httpx.Response(
            200,
            json={
                "model": "doubao-embedding-vision-test",
                "data": {"object": "embedding", "embedding": [vector]},
                "usage": {"total_tokens": 2},
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = OpenAICompatibleEmbeddingProvider(
        OpenAICompatibleEmbeddingConfig(
            provider="doubao",
            api_key="unit-secret",
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            model="doubao-embedding-vision-test",
            timeout_seconds=3,
        ),
        client=client,
    )

    result = await provider.embed(["服务时间", "语音咨询"], "req-mm-batch")
    await client.aclose()

    assert len(payloads) == 2
    assert result["vectors"] == [[1.0, 0.0], [0.0, 1.0]]
    assert result["dimensions"] == 2
    assert result["usage"] == {"batch_calls": 2, "provider_usage_present": True}
