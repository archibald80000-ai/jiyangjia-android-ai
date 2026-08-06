from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from .config import Settings
from .tts import ProviderCallError, ProviderConfigurationError


GROUNDING_SYSTEM_PROMPT = (
    "你是积养家门店大屏 AI 客服。回答必须简短、准确、口语化。"
    "只能依据已确认资料回答业务事实；不要编造价格、库存、活动、医疗疗效或诊断建议。"
    "资料不足时明确建议转人工。"
)


@dataclass(frozen=True)
class OpenAICompatibleChatConfig:
    provider: str
    api_key: str | None
    base_url: str
    model: str
    timeout_seconds: float
    max_tokens: int
    temperature: float

    @classmethod
    def from_settings(cls, settings: Settings, provider: str) -> "OpenAICompatibleChatConfig":
        normalized = provider.lower().strip()
        if normalized == "deepseek":
            api_key = os.environ.get("DEEPSEEK_API_KEY")
            base_url = os.environ.get("DEEPSEEK_BASE_URL") or settings.deepseek_base_url
            model = os.environ.get("DEEPSEEK_MODEL") or settings.deepseek_model
        elif normalized in {"doubao", "ark", "volcengine"}:
            api_key = os.environ.get("DOUBAO_API_KEY") or os.environ.get("ARK_API_KEY")
            base_url = os.environ.get("DOUBAO_BASE_URL") or os.environ.get("ARK_BASE_URL") or settings.doubao_base_url
            model = os.environ.get("DOUBAO_MODEL") or os.environ.get("ARK_MODEL") or settings.doubao_model
            normalized = "doubao"
        elif normalized in {"openai-compatible", "compatible"}:
            api_key = os.environ.get("OPENAI_COMPATIBLE_API_KEY")
            base_url = os.environ.get("OPENAI_COMPATIBLE_BASE_URL") or settings.openai_compatible_base_url
            model = os.environ.get("OPENAI_COMPATIBLE_MODEL") or settings.openai_compatible_model
            normalized = "openai-compatible"
        else:
            raise ProviderConfigurationError([f"UNSUPPORTED_LLM_PROVIDER:{provider}"])

        missing = []
        if not api_key:
            missing.append(_api_key_name_for_chat(normalized))
        if not base_url:
            missing.append(_base_url_name_for_chat(normalized))
        if not model:
            missing.append(_model_name_for_chat(normalized))
        if missing:
            raise ProviderConfigurationError(missing)
        return cls(
            provider=normalized,
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout_seconds=settings.llm_timeout_seconds,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
        )


class OpenAICompatibleLLMProvider:
    def __init__(self, config: OpenAICompatibleChatConfig, client: httpx.AsyncClient | None = None) -> None:
        self.name = config.provider
        self.config = config
        self._client = client

    async def chat(self, messages: list[dict[str, str]], context: list[dict[str, object]], request_id: str) -> dict[str, object]:
        if not messages:
            raise ProviderCallError("LLM_EMPTY_MESSAGES", "messages must not be empty", retryable=False)
        payload = {
            "model": self.config.model,
            "messages": _build_grounded_messages(messages, context),
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": False,
        }
        response = await self._post_json(_endpoint(self.config.base_url, "chat/completions"), payload, request_id)
        text = _extract_chat_text(response)
        answer = text[:600]
        return {
            "text": answer,
            "provider": self.name,
            "model": response.get("model") or self.config.model,
            "source": "knowledge_grounded" if context else "human_handoff",
            "subtitles": _split_subtitles(answer),
            "usage": response.get("usage") if isinstance(response.get("usage"), dict) else None,
        }

    async def _post_json(self, endpoint: str, payload: dict[str, Any], request_id: str) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "X-Request-Id": request_id,
        }
        timeout = httpx.Timeout(self.config.timeout_seconds)
        last_error: ProviderCallError | None = None
        for attempt in range(2):
            try:
                if self._client is not None:
                    response = await self._client.post(endpoint, json=payload, headers=headers, timeout=timeout)
                else:
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.post(endpoint, json=payload, headers=headers)
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_error = ProviderCallError("LLM_PROVIDER_UNAVAILABLE", "LLM provider network failure", retryable=True)
                if attempt == 0:
                    continue
                raise last_error from exc
            if response.status_code >= 500 and attempt == 0:
                last_error = ProviderCallError("LLM_PROVIDER_UNAVAILABLE", "LLM provider unavailable", retryable=True)
                continue
            if response.status_code >= 500:
                raise ProviderCallError("LLM_PROVIDER_UNAVAILABLE", "LLM provider unavailable", retryable=True)
            if response.status_code >= 400:
                raise ProviderCallError("LLM_PROVIDER_REJECTED", _safe_provider_error("LLM provider rejected the request", response), retryable=False)
            try:
                parsed = response.json()
            except ValueError as exc:
                raise ProviderCallError("LLM_BAD_RESPONSE", "LLM provider returned invalid JSON", retryable=True) from exc
            if not isinstance(parsed, dict):
                raise ProviderCallError("LLM_BAD_RESPONSE", "LLM provider returned a non-object JSON response", retryable=True)
            return parsed
        if last_error:
            raise last_error
        raise ProviderCallError("LLM_PROVIDER_UNAVAILABLE", "LLM provider unavailable", retryable=True)


@dataclass(frozen=True)
class OpenAICompatibleEmbeddingConfig:
    provider: str
    api_key: str | None
    base_url: str
    model: str
    timeout_seconds: float

    @classmethod
    def from_settings(cls, settings: Settings, provider: str) -> "OpenAICompatibleEmbeddingConfig":
        normalized = provider.lower().strip()
        if normalized in {"doubao", "ark", "volcengine"}:
            api_key = os.environ.get("DOUBAO_EMBEDDING_API_KEY") or os.environ.get("EMBEDDING_API_KEY") or os.environ.get("DOUBAO_API_KEY") or os.environ.get("ARK_API_KEY")
            base_url = os.environ.get("DOUBAO_EMBEDDING_BASE_URL") or os.environ.get("EMBEDDING_BASE_URL") or os.environ.get("DOUBAO_BASE_URL") or os.environ.get("ARK_BASE_URL") or settings.doubao_embedding_base_url
            model = os.environ.get("DOUBAO_EMBEDDING_MODEL") or os.environ.get("EMBEDDING_MODEL") or settings.doubao_embedding_model
            normalized = "doubao"
        elif normalized in {"openai-compatible", "compatible"}:
            api_key = os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_API_KEY") or os.environ.get("EMBEDDING_API_KEY") or os.environ.get("OPENAI_COMPATIBLE_API_KEY")
            base_url = os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_BASE_URL") or os.environ.get("EMBEDDING_BASE_URL") or os.environ.get("OPENAI_COMPATIBLE_BASE_URL") or settings.openai_compatible_embedding_base_url
            model = os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_MODEL") or os.environ.get("EMBEDDING_MODEL") or settings.openai_compatible_embedding_model
            normalized = "openai-compatible"
        else:
            raise ProviderConfigurationError([f"UNSUPPORTED_EMBEDDING_PROVIDER:{provider}"])

        missing = []
        if not api_key:
            missing.append(_api_key_name_for_embedding(normalized))
        if not base_url:
            missing.append(_base_url_name_for_embedding(normalized))
        if not model:
            missing.append(_model_name_for_embedding(normalized))
        if missing:
            raise ProviderConfigurationError(missing)
        return cls(
            provider=normalized,
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout_seconds=settings.embedding_timeout_seconds,
        )


class OpenAICompatibleEmbeddingProvider:
    def __init__(self, config: OpenAICompatibleEmbeddingConfig, client: httpx.AsyncClient | None = None) -> None:
        self.name = config.provider
        self.config = config
        self._client = client

    async def embed(self, texts: list[str], request_id: str) -> dict[str, object]:
        clean_texts = [text.strip() for text in texts if text and text.strip()]
        if not clean_texts:
            raise ProviderCallError("EMBEDDING_EMPTY_TEXT", "texts must not be empty", retryable=False)
        if _embedding_route(self.config.model) == "embeddings/multimodal" and len(clean_texts) > 1:
            return await self._embed_multimodal_batch(clean_texts, request_id)
        payload = {
            "model": self.config.model,
            "input": _embedding_input(self.config.model, clean_texts),
        }
        response = await self._post_json(_endpoint(self.config.base_url, _embedding_route(self.config.model)), payload, request_id)
        vectors = _extract_embedding_vectors(response, expected_count=len(clean_texts))
        dimensions = len(vectors[0]) if vectors else 0
        return {
            "provider": self.name,
            "model": response.get("model") or self.config.model,
            "vectors": vectors,
            "dimensions": dimensions,
            "usage": response.get("usage") if isinstance(response.get("usage"), dict) else None,
        }

    async def _embed_multimodal_batch(self, clean_texts: list[str], request_id: str) -> dict[str, object]:
        vectors: list[list[float]] = []
        usage_present = False
        model = self.config.model
        endpoint = _endpoint(self.config.base_url, "embeddings/multimodal")
        for index, text in enumerate(clean_texts):
            payload = {
                "model": self.config.model,
                "input": _embedding_input(self.config.model, [text]),
            }
            response = await self._post_json(endpoint, payload, f"{request_id}-{index}")
            vectors.extend(_extract_embedding_vectors(response, expected_count=1))
            model = str(response.get("model") or model)
            usage_present = usage_present or isinstance(response.get("usage"), dict)
        dimensions = len(vectors[0]) if vectors else 0
        return {
            "provider": self.name,
            "model": model,
            "vectors": vectors,
            "dimensions": dimensions,
            "usage": {"batch_calls": len(clean_texts), "provider_usage_present": usage_present},
        }

    async def _post_json(self, endpoint: str, payload: dict[str, Any], request_id: str) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "X-Request-Id": request_id,
        }
        timeout = httpx.Timeout(self.config.timeout_seconds)
        try:
            if self._client is not None:
                response = await self._client.post(endpoint, json=payload, headers=headers, timeout=timeout)
            else:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(endpoint, json=payload, headers=headers)
        except (httpx.TimeoutException, httpx.TransportError) as exc:
            raise ProviderCallError("EMBEDDING_PROVIDER_UNAVAILABLE", "Embedding provider network failure", retryable=True) from exc
        if response.status_code >= 500:
            raise ProviderCallError("EMBEDDING_PROVIDER_UNAVAILABLE", "Embedding provider unavailable", retryable=True)
        if response.status_code >= 400:
            raise ProviderCallError("EMBEDDING_PROVIDER_REJECTED", _safe_provider_error("Embedding provider rejected the request", response), retryable=False)
        try:
            parsed = response.json()
        except ValueError as exc:
            raise ProviderCallError("EMBEDDING_BAD_RESPONSE", "Embedding provider returned invalid JSON", retryable=True) from exc
        if not isinstance(parsed, dict):
            raise ProviderCallError("EMBEDDING_BAD_RESPONSE", "Embedding provider returned a non-object JSON response", retryable=True)
        return parsed


def _build_grounded_messages(messages: list[dict[str, str]], context: list[dict[str, object]]) -> list[dict[str, str]]:
    grounded = [{"role": "system", "content": GROUNDING_SYSTEM_PROMPT}]
    if context:
        excerpts = []
        for item in context[:3]:
            title = str(item.get("title") or item.get("id") or "未命名资料")
            excerpt = str(item.get("excerpt") or item.get("text") or "")[:500]
            if excerpt:
                excerpts.append(f"- {title}: {excerpt}")
        grounded.append({"role": "system", "content": "已确认资料：\n" + "\n".join(excerpts)})
    else:
        grounded.append({"role": "system", "content": "当前没有命中的已确认资料；除非是寒暄，否则请建议转人工确认。"})
    grounded.extend(messages)
    return grounded


def _extract_chat_text(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ProviderCallError("LLM_NO_TEXT", "LLM response did not include choices", retryable=True)
    first = choices[0]
    if not isinstance(first, dict):
        raise ProviderCallError("LLM_BAD_RESPONSE", "LLM choice was not an object", retryable=True)
    message = first.get("message")
    content = message.get("content") if isinstance(message, dict) else first.get("text")
    if not isinstance(content, str) or not content.strip():
        raise ProviderCallError("LLM_NO_TEXT", "LLM response did not include text", retryable=True)
    return content.strip()


def _extract_embedding_vectors(response: dict[str, Any], expected_count: int) -> list[list[float]]:
    data = response.get("data")
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or len(data) < expected_count:
        raise ProviderCallError("EMBEDDING_NO_VECTOR", "Embedding response did not include enough vectors", retryable=True)
    vectors: list[list[float]] = []
    for item in data[:expected_count]:
        if not isinstance(item, dict):
            raise ProviderCallError("EMBEDDING_BAD_RESPONSE", "Embedding item was not an object", retryable=True)
        vector = item.get("embedding")
        if _is_nested_single_vector(vector):
            vector = vector[0]
        if not isinstance(vector, list) or not vector:
            raise ProviderCallError("EMBEDDING_NO_VECTOR", "Embedding item did not include a vector", retryable=True)
        try:
            vectors.append([float(value) for value in vector])
        except (TypeError, ValueError) as exc:
            raise ProviderCallError("EMBEDDING_BAD_VECTOR", "Embedding vector contained a non-numeric value", retryable=True) from exc
    dimensions = {len(vector) for vector in vectors}
    if len(dimensions) != 1:
        raise ProviderCallError("EMBEDDING_BAD_VECTOR", "Embedding vectors had inconsistent dimensions", retryable=True)
    return vectors


def _split_subtitles(text: str, max_chars: int = 80) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    return [text[index : index + max_chars] for index in range(0, len(text), max_chars)]


def _embedding_route(model: str) -> str:
    normalized = model.lower()
    if "vision" in normalized or "multimodal" in normalized:
        return "embeddings/multimodal"
    return "embeddings"


def _embedding_input(model: str, texts: list[str]) -> list[str] | list[dict[str, str]]:
    normalized = model.lower()
    if "vision" in normalized or "multimodal" in normalized:
        return [{"type": "text", "text": text} for text in texts]
    return texts


def _is_nested_single_vector(vector: Any) -> bool:
    return (
        isinstance(vector, list)
        and len(vector) == 1
        and isinstance(vector[0], list)
        and bool(vector[0])
    )


def _endpoint(base_url: str, route: str) -> str:
    normalized = base_url.strip().rstrip("/")
    for suffix in ("/chat/completions", "/embeddings"):
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)].rstrip("/")
    if normalized.endswith("/" + route):
        return normalized
    return f"{normalized}/{route}"


def _safe_provider_error(prefix: str, response: httpx.Response) -> str:
    details = [f"http_status={response.status_code}"]
    try:
        payload = response.json()
    except ValueError:
        return f"{prefix}; {'; '.join(details)}"
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict):
            code = error.get("code")
            error_type = error.get("type")
        else:
            code = payload.get("code")
            error_type = payload.get("type")
        if code:
            details.append(f"provider_code={code}")
        if error_type:
            details.append(f"provider_type={error_type}")
    return f"{prefix}; {'; '.join(details)}"


def _api_key_name_for_chat(provider: str) -> str:
    if provider == "deepseek":
        return "DEEPSEEK_API_KEY"
    if provider == "doubao":
        return "DOUBAO_API_KEY or ARK_API_KEY"
    return "OPENAI_COMPATIBLE_API_KEY"


def _base_url_name_for_chat(provider: str) -> str:
    if provider == "deepseek":
        return "DEEPSEEK_BASE_URL"
    if provider == "doubao":
        return "DOUBAO_BASE_URL or ARK_BASE_URL"
    return "OPENAI_COMPATIBLE_BASE_URL"


def _model_name_for_chat(provider: str) -> str:
    if provider == "deepseek":
        return "DEEPSEEK_MODEL"
    if provider == "doubao":
        return "DOUBAO_MODEL or ARK_MODEL"
    return "OPENAI_COMPATIBLE_MODEL"


def _api_key_name_for_embedding(provider: str) -> str:
    if provider == "doubao":
        return "DOUBAO_EMBEDDING_API_KEY or EMBEDDING_API_KEY or DOUBAO_API_KEY or ARK_API_KEY"
    return "OPENAI_COMPATIBLE_EMBEDDING_API_KEY or EMBEDDING_API_KEY or OPENAI_COMPATIBLE_API_KEY"


def _base_url_name_for_embedding(provider: str) -> str:
    if provider == "doubao":
        return "DOUBAO_EMBEDDING_BASE_URL or EMBEDDING_BASE_URL or DOUBAO_BASE_URL or ARK_BASE_URL"
    return "OPENAI_COMPATIBLE_EMBEDDING_BASE_URL or EMBEDDING_BASE_URL or OPENAI_COMPATIBLE_BASE_URL"


def _model_name_for_embedding(provider: str) -> str:
    if provider == "doubao":
        return "DOUBAO_EMBEDDING_MODEL or EMBEDDING_MODEL"
    return "OPENAI_COMPATIBLE_EMBEDDING_MODEL or EMBEDDING_MODEL"
