# MVP API Spec

Updated: 2026-08-06

Base path: `/api/v1`

## Common Rules

- Every response includes or echoes `request_id` when meaningful.
- Gateway returns `X-Request-Id`.
- Android sends `X-Device-Id` when configured.
- `Authorization` may carry a device token, but it is never logged.
- Provider secrets are server-side only and loaded from `.env.local` or server environment.

## Required Endpoints

- `GET /health`
- `GET /api/v1/health`
- `POST /api/v1/dialogue/text`
- `POST /api/v1/dialogue/audio`
- `POST /api/v1/knowledge/index`
- `POST /api/v1/knowledge/search`
- `GET /api/v1/knowledge/status`
- `GET /api/v1/audio/{audio_id}`
- `GET /api/v1/client/config`

## Health

`GET /health` and `GET /api/v1/health`

```json
{
  "ok": true,
  "service": "jiyangjia-gateway",
  "version": "0.1.0-task008",
  "providers": {
    "asr": "mock",
    "tts": "mock",
    "llm": "mock",
    "embedding": "mock",
    "knowledge": "sqlite_lightweight"
  }
}
```
## Client Config

`GET /api/v1/client/config`

```json
{
  "display_mode": "idle_video_voice",
  "max_record_seconds": 20,
  "max_upload_bytes": 5242880,
  "accepted_audio_types": ["audio/wav", "audio/mpeg", "audio/mp4", "audio/aac", "audio/webm"],
  "subtitle_max_chars": 80,
  "idle_video_version": "local"
}
```

## Text Dialogue

`POST /api/v1/dialogue/text`

```json
{
  "session_id": "sess_demo",
  "request_id": "optional-client-request-id",
  "text": "服务时间是什么？"
}
```

## Audio Dialogue

`POST /api/v1/dialogue/audio`

Content type: `multipart/form-data`

Fields:

- `session_id`
- `request_id`
- `duration_ms`
- `sample_rate`
- `input_device`
- `audio`

The endpoint validates size and content type, then runs:

```text
ASR -> RAG search -> LLM -> TTS -> audio_id
```

TASK-008 uses Mock providers only. TASK-009 to TASK-012 replace each provider with real adapters.

## Dialogue Response

```json
{
  "request_id": "uuid",
  "session_id": "sess_demo",
  "transcript": {"text": "服务时间是什么？", "provider": "text"},
  "knowledge": {"status": "matched", "matches": []},
  "answer": {"text": "回答文本", "provider": "mock", "subtitles": ["回答文本"]},
  "tts": {"provider": "mock", "content_type": "audio/wav", "audio_id": "aud_...", "duration_ms": 1800},
  "sources": []
}
```

## Knowledge Index

`POST /api/v1/knowledge/index`

```json
{
  "documents": [
    {
      "id": "faq-001",
      "title": "服务时间",
      "text": "门店服务时间请以当天现场公告为准。",
      "status": "approved",
      "source_uri": "manual://faq-001"
    }
  ]
}
```

Accepted statuses: `approved`, `draft`, `rejected`.

## Knowledge Search

`POST /api/v1/knowledge/search`

```json
{
  "query": "服务时间",
  "top_k": 3,
  "include_draft": false
}
```

Response includes `matches`, `sources` and `request_id`. Customer-facing answers may use `approved` sources only.

## Knowledge Status

`GET /api/v1/knowledge/status`

Reports document counts and index readiness. It must not expose raw private documents.

## Audio Fetch

`GET /api/v1/audio/{audio_id}`

Returns generated TTS audio bytes, or a safe `AUDIO_NOT_FOUND` error when expired.

## Error Response

```json
{
  "request_id": "uuid",
  "error": {
    "code": "PROVIDER_TIMEOUT",
    "message_for_user": "现在网络有点忙，请稍后再试。",
    "retryable": true,
    "details": {}
  }
}
```
