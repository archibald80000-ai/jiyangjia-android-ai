# API contracts — draft

## Gateway

### `GET /api/v1/health`

Returns gateway version, provider readiness and dependency status without secrets.

### `POST /api/v1/sessions`

Creates a store/client session and returns a scoped session token.

### `POST /api/v1/dialogue/audio`

Multipart audio request. Response includes:

```json
{
  "request_id": "uuid",
  "session_id": "uuid",
  "recognized_text": "...",
  "answer_text": "...",
  "audio_url": "/api/v1/audio/uuid",
  "need_human": false,
  "display_mode": "idle_video",
  "sources": []
}
```

### `POST /api/v1/dialogue/text`

Development and administration test endpoint; not exposed anonymously in production.

### `GET /api/v1/client/config`

Returns non-secret device configuration, display mode, URLs and feature flags.

### `POST /api/v1/client/status`

Reports app version, device state, microphone selection, network and last error.

## LiveTalking upstream

The integration client targets the upstream contracts at the locked commit, including `/offer`, `/whep`, `/human`, `/humanaudio`, `/interrupt_talk`, `/is_speaking`, `/record`, `/set_audiotype` and `/sse`.

## Contract rules

- OpenAPI is generated from implementation later.
- Error responses include a stable code and request ID.
- No API returns provider secrets or stack traces to Android.
- Audio URLs are short-lived or authenticated.
