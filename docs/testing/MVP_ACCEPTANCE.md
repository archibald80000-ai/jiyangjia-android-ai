# MVP Acceptance

Updated: 2026-08-06

## Release Gate

The Phase 1 MVP is accepted only when the Android 12 store display can complete a real tap-to-talk voice FAQ loop:

```text
idle video -> record -> upload -> ASR -> FAQ/LLM answer -> TTS -> playback + subtitle -> idle
```

## Required Evidence

- APK path, size and SHA-256.
- Android device model, firmware, ABI, display resolution and Android version.
- USB/default microphone enumeration and real recording evidence.
- Speaker playback evidence.
- Gateway health and dialogue request logs with request IDs.
- ASR/TTS/LLM provider configuration status and real call result, or explicit credential blocker.
- FAQ evaluation report.
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

## Gateway Acceptance

- `/api/v1/health` and `/api/v1/client/config` work.
- Audio upload validates type, size and duration.
- Request ID appears in every log line for a dialogue turn.
- Temporary audio is deleted after processing.
- Provider errors map to safe user messages.
- Tests cover happy path, unknown question, provider timeout and prohibited topic.

## Knowledge Acceptance

- 10-30 approved FAQ entries.
- No bulk scan of `E:\work\积养家`.
- Unknown/sensitive questions fall back safely.
- Evaluation report lists pass/fail examples.

## Provider Acceptance

- Doubao ASR and TTS use server-side secrets only.
- LLM provider is configurable and bounded.
- Real paid calls use a small approved test set.
- Missing credentials produce `BLOCKED_PROVIDER_CREDENTIALS`, not fake success.

## Non-Acceptance

The following do not count as Phase 1 completion:

- Mock-only loop presented as real provider success.
- APK build without actual install/run evidence for final device acceptance.
- LiveTalking/WebRTC evidence without the Android voice FAQ loop.
- FAQ generated from unreviewed raw materials.
