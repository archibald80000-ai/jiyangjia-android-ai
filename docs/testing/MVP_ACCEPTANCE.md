# MVP Acceptance

Updated: 2026-08-06

## Release Gate

The Phase 1 MVP is accepted only when the Android 12 large display can complete a real tap-to-talk voice RAG loop:

```text
idle video -> record -> upload -> Doubao ASR -> lightweight RAG -> LLM answer -> Doubao TTS -> playback + subtitle -> idle
```

## Required Evidence

- APK path, size and SHA-256.
- Android device model, firmware, ABI, display resolution and Android version.
- USB/default microphone enumeration and real recording evidence.
- Speaker playback evidence.
- Gateway health and dialogue request logs with request IDs.
- Real Doubao ASR/TTS provider evidence, or explicit credential blocker.
- Real Doubao/Volcengine Ark LLM evidence and OpenAI-compatible fallback evidence, or explicit credential blocker.
- Real Embedding API evidence, or explicit credential blocker.
- Lightweight RAG evaluation report with sources.
- 30-cycle controlled dialogue test or documented blocker.
- Sanitized Android logcat and Gateway logs.

## Android Acceptance

- App launches after install.
- Landscape immersive display.
- Idle video/fallback visible without network.
- Start consultation button works.
- Permission denial handled.
- USB mic preferred when available; default mic fallback works.
- Playback and subtitles are synchronized enough for store use.
- Network/provider failures return to idle without blank screen.

Android real-device acceptance is scheduled for TASK-015 and does not block TASK-008 to TASK-014 local development.

## Gateway Acceptance

- Required endpoints from `docs/api/MVP_API_SPEC.md` work.
- Audio upload validates type, size and duration.
- Request ID appears in each dialogue response and log.
- Temporary/generated audio is fetchable by `audio_id` and expires under the runtime policy.
- Provider errors map to safe user messages.
- Tests cover happy path, unknown question, provider timeout and prohibited topic.

## Knowledge Acceptance

- SQLite metadata and FAISS index are reproducible.
- Markdown/TXT/PDF/DOCX ingestion works only for explicitly selected reviewed files.
- `approved`, `draft`, `rejected` status is enforced.
- Customer-facing answers use `approved` sources only.
- Unknown/sensitive questions fall back safely.
- Evaluation report lists pass/fail examples and source citations.

## Provider Acceptance

- Doubao ASR and TTS use server-side secrets only.
- Doubao/Volcengine Ark LLM and OpenAI-compatible fallback are configurable and bounded.
- Embedding API is behind an adapter.
- Real paid calls use a small approved test set.
- Missing credentials produce `BLOCKED_PROVIDER_CREDENTIALS`, not fake success.

## Non-Acceptance

The following do not count as Phase 1 completion:

- Mock-only loop presented as real provider success.
- APK build without actual install/run evidence for final device acceptance.
- LiveTalking/WebRTC evidence without the Android voice RAG loop.
- RAG generated from unreviewed raw materials.
- Any provider key stored in Android or committed to Git.
