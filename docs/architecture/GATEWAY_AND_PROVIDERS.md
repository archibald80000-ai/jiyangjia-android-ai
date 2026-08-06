# Gateway And Providers

Updated: 2026-08-06

## Responsibility

Gateway owns business orchestration, provider calls, knowledge retrieval, logging, policy and security. Android only captures audio and presents the answer.

## Gateway Modules

- `api`: HTTP endpoints and request/response schemas.
- `sessions`: session lifecycle, request IDs and device identity.
- `audio`: upload validation, temporary storage, format metadata and cleanup.
- `providers.asr`: ASR adapter interface and Doubao/Mock implementations.
- `providers.llm`: LLM adapter interface and configurable provider clients.
- `providers.tts`: TTS adapter interface and Doubao/Mock implementations.
- `knowledge`: small FAQ loader, validator and matcher.
- `policy`: answer limits, prohibited topics, transfer-to-human and error mapping.
- `observability`: structured logs, sanitized provider traces and metrics.
- `config`: environment-driven settings and startup validation.

## Provider Interfaces

Python-style contract:

```python
class ASRProvider:
    async def transcribe(self, audio: bytes, content_type: str, request_id: str) -> dict: ...

class KnowledgeProvider:
    async def search(self, question: str, session_id: str, request_id: str) -> dict: ...

class LLMProvider:
    async def chat(self, messages: list[dict], context: dict | None, request_id: str) -> dict: ...

class TTSProvider:
    async def synthesize(self, text: str, voice_id: str | None, request_id: str) -> dict: ...
```

Provider result shape:

```json
{
  "ok": true,
  "provider": "doubao",
  "latency_ms": 820,
  "data": {},
  "usage": {},
  "error": null
}
```

## Orchestration

1. Validate device/session/auth.
2. Validate audio type, duration and size.
3. Call ASR.
4. Retrieve mini FAQ context.
5. Build LLM prompt with only approved context.
6. Generate concise answer.
7. Call TTS.
8. Return transcript, answer text, knowledge citations/status and audio metadata.
9. Delete temporary audio.

## Error Policy

- `400`: invalid request/audio.
- `401/403`: device auth failure.
- `408`: timeout.
- `413`: audio too large/too long.
- `422`: unsupported audio format.
- `429`: cost/rate limit.
- `502`: provider failure.
- `503`: provider unavailable.

Every error includes `request_id`, `code`, `message_for_user`, `retryable` and sanitized `details`.

## Security

- No provider secrets in Android.
- `.env.local` and server environment variables are never printed.
- Logs redact authorization headers, tokens, cookies, phone numbers and raw customer content where possible.
- Raw audio is temporary by default.
- Provider calls are bounded by timeout, retry count and maximum text/audio duration.

## Deployment Fit

The existing 8C/4G/10M Tencent Cloud server can run this Gateway because Phase 1 has no GPU inference and no realtime video generation.
