# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-014_TENCENT_GATEWAY_DEPLOYMENT.md`
- Current status: `PARTIAL`
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
- TASK-014 server-thread evidence was imported. The Tencent Cloud host `120.53.86.89` now runs commit `f3b406ca28222937a6f4c93bac524c48f0b95544`; health/config/knowledge endpoints are reachable, but dialogue text/audio return `503 BLOCKED_PROVIDER_CREDENTIALS`.
- TASK-014 redeployment package is prepared locally. `deploy/docker-compose.yml` now loads untracked server `secrets/.env.local`, persists `var/knowledge` for SQLite/FAISS and health-checks `/api/v1/health`. The server thread should fix the Provider env chain before retesting dialogue/upload.
- Gateway now exposes `/api/v1/readiness` and returns `failed_stage` for Provider credential failures.
- `scripts/check_provider_env.py` can be run on the server before container restart to verify `secrets/.env.local` and Compose `env_file` without exposing values.

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
- `docs/evidence/TASK-014/task014-redeployment-local-pytest-20260806.txt`
- `docs/evidence/TASK-014/task014-docker-compose-parse-20260806.txt`
- `docs/evidence/TASK-014/task014-redeployment-verify-repository-20260806.txt`

## Not verified

- Formal production knowledge base beyond the scoped demo FAQ set.
- Tencent Cloud Provider env-chain remediation: `/opt/jiyangjia-ai/secrets/.env.local` must exist with mode `600`, Compose `env_file` must point to it, `/api/v1/readiness` must show configured Providers, then dialogue/text and dialogue/audio must each return `request_id`, `sources`, `audio_id` and audio fetch 200.
- Android 12 real-device install/record/upload/playback/subtitle acceptance.
- USB microphone and speaker physical validation.

## Next action

Continue exactly one next task: send the server-management thread the Provider env-chain fix instructions, have it run `scripts/check_provider_env.py`, verify `/api/v1/readiness`, then run one complete text/audio acceptance and return sanitized evidence.

Do not enter `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md` until TASK-014 is no longer partial.
- 2026-08-06：TASK-014 已完成重部署与 200 路径验证；证据已写入 `docs/server/gateway_deployment_report.md` 与 `/opt/jiyangjia-ai/logs/task014_evidence/*`。剩余阻塞为 Provider 凭据缺失，先补齐再执行 TASK-015。
