# MVP API Spec

Updated: 2026-08-07

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
- `GET /api/v1/readiness`
- `POST /api/v1/dialogue/text`
- `POST /api/v1/dialogue/audio`
- `POST /api/v1/knowledge/index`
- `POST /api/v1/knowledge/search`
- `GET /api/v1/knowledge/status`
- `GET /api/v1/audio/{audio_id}`
- `GET /api/v1/client/config`

## TASK-014A Admin and Display Endpoints

Production `/api/v1/admin/*` requests require `X-Admin-Token`. If production has no `ADMIN_TOKEN`, the API fails closed with `503 ADMIN_TOKEN_NOT_CONFIGURED`. The token is never returned to a browser or Android client.

Management pages:

- `GET /admin/system`
- `GET /admin/knowledge`
- `GET /admin/avatar`
- `GET /admin/display`

Admin API:

- `GET /api/v1/admin/system/status`
- `GET /api/v1/admin/knowledge`
- `POST /api/v1/admin/knowledge/upload` (`file`: PDF/DOCX/MD/TXT)
- `POST /api/v1/admin/knowledge/{run_id}/preview`
- `POST /api/v1/admin/knowledge/{run_id}/approve`
- `POST /api/v1/admin/knowledge/{run_id}/reject`
- `POST /api/v1/admin/knowledge/{run_id}/publish`
- `GET|POST /api/v1/admin/avatar`
- `GET /api/v1/admin/avatar/{avatar_id}/file`
- `POST /api/v1/admin/avatar/{avatar_id}/publish`
- `POST /api/v1/admin/avatar/{avatar_id}/rollback`
- `DELETE /api/v1/admin/avatar/{avatar_id}/delete`
- `GET|POST /api/v1/admin/display`
- `PUT /api/v1/admin/display/{profile_id}`
- `POST /api/v1/admin/display/{profile_id}/set-default`

Public client API:

- `GET /api/v1/assets/manifest`
- `GET /api/v1/assets/{avatar_id}` (published assets only)
- `GET /api/v1/display/profile?width=1920&height=1080&orientation=landscape`

Knowledge is not customer-visible after upload or approval alone. Only `publish` changes the parsed documents from `draft` to `approved` and invokes the configured Embedding Provider.

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

## Readiness

`GET /api/v1/readiness`

Reports whether Provider configuration is ready for real dialogue without exposing secret values.

```json
{
  "request_id": "uuid",
  "ready": false,
  "status": "blocked_provider_credentials",
  "providers": {
    "asr": {"provider": "doubao", "ready": false, "missing": ["DOUBAO_ASR_AUTH"]},
    "tts": {"provider": "doubao", "ready": false, "missing": ["DOUBAO_TTS_AUTH"]},
    "llm": {"provider": "doubao", "ready": false, "missing": ["DOUBAO_API_KEY"]},
    "embedding": {"provider": "doubao", "ready": false, "missing": ["DOUBAO_EMBEDDING_API_KEY"]}
  }
}
```

Only configured/missing names may be exposed. Secret values must never appear.

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
    "failed_stage": "asr_provider_call",
    "message_for_user": "现在网络有点忙，请稍后再试。",
    "retryable": true,
    "details": {}
  }
}
```
