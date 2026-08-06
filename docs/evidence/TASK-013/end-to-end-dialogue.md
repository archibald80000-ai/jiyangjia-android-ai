# TASK-013 End-To-End Dialogue Evidence

Updated: 2026-08-06

## Result

TASK-013 is PARTIAL.

Completed locally:

- Android records microphone PCM, wraps it as WAV and uploads to Gateway `/api/v1/dialogue/audio`.
- Android propagates one generated `request_id` through upload, dialogue response and audio fetch.
- Android parses transcript, answer subtitles, `sources`, `audio_id` and TTS content type.
- Android downloads generated TTS audio and plays encoded answer audio through `MediaPlayer`.
- Android keeps idle-video/fallback visual underneath the interaction overlay.
- Android supports cancel during upload/waiting/playback and returns to idle fallback.
- Gateway E2E mock loop covers ASR -> RAG -> LLM -> TTS -> audio fetch with `sources`.
- Gateway real Provider smoke covers real Doubao ASR -> real Doubao/Ark Embedding RAG -> real Doubao/Ark LLM -> real Doubao TTS -> audio fetch.

Not completed:

- Android 12 real-device install, recording, upload, playback and subtitle visual validation.
- Physical USB microphone/speaker validation.
- Store-network latency and reliability validation.

## Android Build Artifact

- APK: `android-app/app/build/outputs/apk/debug/app-debug.apk`
- Size: `862144` bytes
- SHA-256: `263B1FA8E8DB2198E93B4E4FFC85E715CEE2556E0511C67B002D7E588C76BC8E`
- Package: `ai.jiyangjia.kiosk.debug`
- Version: `0.1.0-task013-debug`
- minSdk: `23`
- targetSdk: `35`
- Permissions: `INTERNET`, `ACCESS_NETWORK_STATE`, `RECORD_AUDIO`

## Mock 30-Cycle Report

- Report: `docs/evidence/TASK-013/task013-30cycle-pytest-report.json`
- Cycles: `30`
- Passed: `30`
- Failed: `0`
- Fallback count: `0`
- Local TestClient latency: min `3.17ms`, max `6.07ms`, avg `4.33ms`

This is backend in-process TestClient latency, not Android real-device latency.

## Real Provider Smoke

Input:

- Private env: `E:\work\ai-kefu\.env.local`
- Test audio: `tmp/doubao-tts-test-16k.wav`
- Temporary approved FAQ: `manual://task013/real-provider-smoke`

Result:

```json
{
  "ok": true,
  "request_id": "task013-real-provider-smoke",
  "session_id": "sess-task013-real",
  "providers": {"asr": "doubao", "llm": "doubao", "tts": "doubao"},
  "transcript_text": "您好，欢迎来到季养家。",
  "knowledge_status": "matched",
  "source_count": 1,
  "subtitle_count": 1,
  "answer_chars": 46,
  "audio_status": 200,
  "audio_content_type": "audio/mpeg",
  "audio_bytes": 69741,
  "latency_ms": 13623
}
```

Observed provider calls:

- Doubao/Ark Embedding `/embeddings/multimodal`: HTTP 200
- Doubao/Ark Chat `/chat/completions`: HTTP 200
- Doubao TTS `/api/v3/tts/unidirectional`: HTTP 200

No secret values were printed or committed.

ASR vocabulary mitigation:

- The generated test phrase `您好，欢迎来到积养家。` was recognized as `您好，欢迎来到季养家。` in this TASK-013 run. Earlier TASK-010 observed another homophone variant.
- A follow-up TASK-013 hardening patch now normalizes common `ji/yang/jia` homophones such as `机养家`, `季养家`, `寄养家`, `吉阳家`, `积阳家` and `济氧家` to canonical `积养家`.
- Gateway keeps the original provider text as `transcript.raw_text` when normalization changes the transcript, so debugging evidence is preserved.

Follow-up evidence:

- `docs/evidence/TASK-013/task013-brand-normalization-samples-20260806.txt`
- `docs/evidence/TASK-013/task013-brand-normalization-pytest-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-after-brand-normalization-20260806.txt`

## Verification Logs

- `docs/evidence/TASK-013/task013-pytest-e2e-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-20260806.txt`
- `docs/evidence/TASK-013/task013-android-unit-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-assemble-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-lint-final-20260806.txt`
- `docs/evidence/TASK-013/task013-adb-devices-20260806.txt`
- `docs/evidence/TASK-013/task013-connected-debug-android-test-20260806.txt`

## Hardware Boundary

`adb devices -l` returned no attached devices. Therefore this task does not claim:

- APK installed on Android 12 hardware.
- USB microphone worked on real hardware.
- Speaker playback worked on real hardware.
- Subtitles were visually checked on the store display.
