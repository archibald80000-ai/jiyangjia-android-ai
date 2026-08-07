from __future__ import annotations

from typing import Awaitable, Callable, Protocol


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
            "text": "模拟语音问题",
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
        else:
            answer = "这项信息我暂时不能确认，请咨询现场工作人员。"
            source = "human_handoff"
        return {
            "text": answer[:240],
            "provider": self.name,
            "source": source,
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
