# Gateway And Providers

Updated: 2026-08-06

## Responsibility

Gateway owns business orchestration, provider calls, lightweight RAG retrieval, logging, policy and security. Android only captures audio and presents the answer.

## Modules

- `api`: FastAPI endpoints and schemas.
- `config`: environment-driven settings and safe provider status.
- `providers`: ASR, TTS, LLM and Embedding adapters.
- `knowledge`: SQLite metadata/search skeleton in TASK-008; FAISS Top-K in TASK-012.
- `audio_store`: temporary generated audio lookup by `audio_id`.
- `policy`: no-claim rules, transfer-to-human and safe error mapping.
- `observability`: request IDs and sanitized logs.

## Required Provider Interfaces

```python
class ASRProvider:
    async def transcribe(self, audio: bytes, content_type: str, request_id: str) -> dict: ...

class TTSProvider:
    async def synthesize(self, text: str, voice_id: str | None, request_id: str) -> dict: ...

class LLMProvider:
    async def chat(self, messages: list[dict], context: list[dict], request_id: str) -> dict: ...

class EmbeddingProvider:
    async def embed(self, texts: list[str], request_id: str) -> dict: ...
```

## Real Provider Sequence

- TASK-008 creates Mock providers and stable API contracts.
- TASK-009 adds real Doubao TTS.
- TASK-010 adds real Doubao ASR.
- TASK-011 adds real Doubao/Volcengine Ark LLM, OpenAI-compatible fallback and Embedding API.
- TASK-012 uses EmbeddingProvider with SQLite and FAISS for lightweight RAG.

## Security

- Android never stores provider secrets.
- `.env.local` is never read into logs or committed.
- Diagnostics may report only `configured`, `missing` or `disabled`.
- Provider calls must have timeout, finite retry and cost controls.
- Logs must include request IDs and avoid raw tokens, cookies, recordings and private documents.
