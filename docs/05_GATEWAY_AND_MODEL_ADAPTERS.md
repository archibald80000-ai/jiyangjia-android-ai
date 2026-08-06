# Gateway and provider adapters

## Gateway goals

A lightweight service suitable for 4 GB RAM. Initial implementation can use FastAPI, SQLite and simple structured logs. It must not host a large model or heavy vector database.

## Core interfaces

```python
class ASRProvider:
    async def transcribe(self, audio: bytes, content_type: str) -> TranscriptionResult: ...

class TTSProvider:
    async def synthesize(self, text: str, voice_id: str | None) -> SpeechResult: ...

class LLMProvider:
    async def chat(self, messages: list[Message], context: str | None) -> LLMResult: ...

class KnowledgeProvider:
    async def answer(self, question: str, session_id: str, store_id: str) -> KnowledgeResult: ...

class LiveTalkingClient:
    async def speak_text(self, session_id: str, text: str, interrupt: bool) -> None: ...
```

These are interface contracts, not proof of implementation. `LiveTalkingClient` is a future extension point and is not part of Phase 1 execution.

## Provider order

- ASR: fixed-text test → Mock → Doubao.
- TTS: generated test audio → Mock → Doubao.
- LLM: Mock → one OpenAI-compatible route → Doubao/Qwen alternatives.
- Knowledge: mini FAQ → optional LLM fallback → formal RAG later.

## Reliability

- Per-provider timeouts.
- At most one automatic retry for chargeable calls unless documented otherwise.
- Circuit-breaker or cool-down for repeated failures.
- `request_id` propagation.
- User-safe error mapping.
- No provider response or raw secret in normal logs.
