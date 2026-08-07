# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-014A_ADMIN_CONTENT_DISPLAY.md`
- Current status: `PLANNED`
- Current branch: `task/TASK-014-tencent-gateway-deployment`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## TASK-013 implemented

- Android `GatewayClient` submits recorded PCM as WAV multipart to Gateway `/api/v1/dialogue/audio`.
- Android carries one `request_id` through dialogue upload and generated audio fetch.
- Android parses transcript, answer subtitles, `sources`, `audio_id` and TTS content type.
- Android downloads `/api/v1/audio/{audio_id}` and plays encoded response audio through `MediaPlayer`.
- Android state machine now shows uploading, waiting, playing, cancel and service-error states before returning to idle-video/fallback.
- `tests/e2e/test_dialogue_loop.py` covers Mock Gateway ASR -> RAG -> LLM -> TTS -> audio fetch.
- 30-cycle Mock Gateway report is generated at `docs/evidence/TASK-013/task013-30cycle-pytest-report.json`.
- Gateway transcript normalization now maps common ASR brand homophones (`机养家`, `季养家`, `寄养家`, `吉阳家`, `积阳家`, `济氧家`) to canonical `积养家` before RAG/LLM while preserving `transcript.raw_text`.

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\e2e -q`: 3 passed.
- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\e2e tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q`: 37 passed.
- Mock 30-cycle Gateway dialogue report: 30 passed, 0 failed, 0 fallback.
- Real private-env Gateway smoke passed with Doubao ASR, Doubao/Ark Embedding RAG, Doubao/Ark LLM and Doubao TTS; generated TTS audio fetch returned `audio/mpeg`, `69741` bytes.
- Android `testDebugUnitTest`, `assembleDebug` and `lintDebug` passed using project-local Temurin JDK 17.
- APK: `android-app\app\build\outputs\apk\debug\app-debug.apk`, version `0.1.0-task013-debug`, size `862144`, SHA-256 `263B1FA8E8DB2198E93B4E4FFC85E715CEE2556E0511C67B002D7E588C76BC8E`.
- `adb devices -l` returned no attached devices.
- Brand normalization tests passed: `python -m pytest tests\asr tests\gateway tests\e2e -q` -> 19 passed; full backend regression -> 42 passed.
- TASK-014 now passes the real MVP chain on `120.53.86.89` with `env_file` aligned to `/opt/jiyangjia-ai/secrets/.env.local` and `readiness` all ready.
- Gateway exposes `/api/v1/readiness`, and `scripts/check_provider_env.py --require-real-mvp` is available for CI-like preflight.
- `task014-acceptance-summary-20260807-0943.json`, `task014-dialogue-audio-retry-20260807-0944.json` and `task014-provider-env-check-after-recreate-20260807.json` contain the final production evidence.

## Evidence

- `docs/evidence/TASK-013/end-to-end-dialogue.md`
- `docs/evidence/TASK-013/task013-30cycle-pytest-report.json`
- `docs/evidence/TASK-013/task013-pytest-e2e-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-20260806.txt`
- `docs/evidence/TASK-013/task013-android-unit-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-assemble-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-lint-final-20260806.txt`
- `docs/evidence/TASK-013/task013-apk-verification-20260806.txt`
- `docs/evidence/TASK-013/task013-brand-normalization-samples-20260806.txt`
- `docs/evidence/TASK-013/task013-brand-normalization-pytest-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-after-brand-normalization-20260806.txt`
- `docs/evidence/TASK-014/server-evidence-reconciliation-20260806.md`
- `docs/evidence/TASK-014/server-redeployment-request-20260806.md`
- `docs/evidence/TASK-014/task014-provider-env-check-after-recreate-20260807.json`
- `docs/evidence/TASK-014/task014-acceptance-summary-20260807-0943.json`
- `docs/evidence/TASK-014/task014-dialogue-audio-retry-20260807-0944.json`
- `docs/evidence/TASK-014/task014-redeployment-local-pytest-20260806.txt`
- `docs/evidence/TASK-014/task014-docker-compose-parse-20260806.txt`
- `docs/evidence/TASK-014/task014-redeployment-verify-repository-20260806.txt`

## Not verified

- Formal production knowledge base beyond the scoped demo FAQ set.
- Android 12 real-device install/record/upload/playback/subtitle acceptance.
- USB microphone and speaker physical validation.

## Next action

Complete one next task: prepare TASK-014A admin skeleton and display-profile contracts in `tasks/TASK-014A_ADMIN_CONTENT_DISPLAY.md`.
- 2026-08-07：TASK-014 收口完成；下一步进入 `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md` 前先完成 `TASK-014A` 方案沉淀。
