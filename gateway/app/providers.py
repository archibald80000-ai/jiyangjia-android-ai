from __future__ import annotations

from typing import Awaitable, Callable, Protocol

from .answer_policy import classify_answer_scope, latest_user_text
from .persona import PERSONA_VERSION, response_mode


class ASRProvider(Protocol):
    name: str

    async def transcribe(self, audio: bytes, content_type: str, request_id: str) -> dict[str, object]: ...


class StreamingASRSession(Protocol):
    async def push(self, pcm_frame: bytes) -> list[str]: ...

    async def finish(self) -> dict[str, object]: ...

    async def close(self) -> None: ...


class StreamingASRProvider(Protocol):
    name: str

    async def open_stream(self, request_id: str) -> StreamingASRSession: ...


class LLMProvider(Protocol):
    name: str

    async def chat(self, messages: list[dict[str, str]], context: list[dict[str, object]], request_id: str) -> dict[str, object]: ...


class TTSProvider(Protocol):
    name: str

    async def synthesize(self, text: str, voice_id: str | None, request_id: str) -> dict[str, object]: ...


class EmbeddingProvider(Protocol):
    name: str

    async def embed(self, texts: list[str], request_id: str) -> dict[str, object]: ...


class MockASRProvider:
    name = "mock"

    async def transcribe(self, audio: bytes, content_type: str, request_id: str) -> dict[str, object]:
        return {
            "text": "积养家模拟语音问题",
            "provider": self.name,
            "language": "zh-CN",
            "confidence": 1.0 if audio else 0.0,
            "content_type": content_type,
        }


class MockLLMProvider:
    name = "mock"

    async def chat(self, messages: list[dict[str, str]], context: list[dict[str, object]], request_id: str) -> dict[str, object]:
        user_text = messages[-1]["content"] if messages else ""
        if context:
            answer = f"根据已确认资料：{context[0].get('excerpt', '')}"
            source = "knowledge_grounded_mock"
        elif classify_answer_scope(latest_user_text(messages)) == "jiyangjia":
            answer = "这项积养家相关信息没有已确认资料，我暂时不能确认，请咨询现场工作人员。"
            source = "in_domain_unverified"
        else:
            answer = f"这是一个通用问题：{user_text}。请结合实际情况判断。"
            source = "general_answer_mock"
        return {
            "text": answer[:240],
            "provider": self.name,
            "source": source,
            "persona": PERSONA_VERSION,
            "response_mode": response_mode(user_text),
            "subtitles": [answer[:80]],
            "input": user_text[:80],
        }


class MockTTSProvider:
    name = "mock"

    async def synthesize(self, text: str, voice_id: str | None, request_id: str) -> dict[str, object]:
        return {
            "provider": self.name,
            "content": b"MOCK_TTS_AUDIO",
            "content_type": "audio/wav",
            "duration_ms": max(300, min(5000, len(text) * 90)),
            "voice_id": voice_id or "mock",
        }


class MockEmbeddingProvider:
    name = "mock"

    async def embed(self, texts: list[str], request_id: str) -> dict[str, object]:
        return {
            "provider": self.name,
            "vectors": [[float(len(text) % 17)] for text in texts],
            "dimensions": 1,
        }
