# TASK-009 TTS Provider Evidence

Date: 2026-08-06

## Official Documentation Checked

Official Volcengine/Doubao documentation entry points checked on 2026-08-06:

- `https://api.volcengine.com/api-docs/view?serviceCode=speech_saas_prod&version=2025-05-20&action=ListSpeakers` - Speech SaaS OpenAPI `ListSpeakers` entry provided by the user, used for current speaker/resource management reference.
- `https://www.volcengine.com/docs/6561/2528925` - Doubao speech HTTP unidirectional streaming synthesis.
- `https://www.volcengine.com/docs/6561/1719100` - Doubao speech WebSocket unidirectional streaming V3.
- `https://www.volcengine.com/docs/6561/1598757` - Doubao speech HTTP Chunked/SSE unidirectional streaming V3.
- `https://www.volcengine.com/docs/6561/1257584` - speech synthesis HTTP API.
- `https://www.volcengine.com/docs/6561/97465` - TTS access and parameter documentation entry.

Implementation now prefers the official V3 HTTP unidirectional streaming shape and keeps the legacy V1 HTTP shape as compatibility fallback:

- default endpoint: `https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- auth headers: either `X-Api-Key`, or `X-Api-App-Id` + `X-Api-Access-Key`
- required model/billing selector: `X-Api-Resource-Id`
- request correlation: `X-Api-Request-Id`
- body fields: `user.uid`, `req_params.text`, `req_params.speaker`, `req_params.audio_params`
- response parser: concatenated JSON stream frames with base64 audio chunks and final code `20000000`

Legacy V1 compatibility retained:

- endpoint: `https://openspeech.bytedance.com/api/v1/tts`
- authorization header: `Bearer; <access_token>`
- app fields: `appid`, `token`, `cluster`
- audio fields: `voice_type`, `encoding`, `speed_ratio`, `volume_ratio`, `pitch_ratio`
- request fields: `reqid`, `text`, `text_type`, `operation=query`

## Implemented

- Added `DoubaoTTSConfig` and `DoubaoTTSProvider`.
- Added V3 unidirectional TTS payload/header support.
- Added V3 concatenated JSON stream frame parsing.
- Kept V1 HTTP endpoint compatibility.
- Added missing-credential error: `BLOCKED_PROVIDER_CREDENTIALS`.
- Added safe provider call error mapping.
- Added CLI test helper: `scripts/test_tts_provider.py`.
- Added CLI `--env-file` support for private external env files.
- Added CLI config preflight: `scripts/test_tts_provider.py --provider doubao --check-config`.
- Updated `.env.example` with current TASK-009 TTS variable names and placeholders only.
- Added TTS tests under `tests/tts/`.
- Gateway no longer silently downgrades a configured Doubao TTS provider to Mock when credentials are missing.

## Verification

- `docs/evidence/TASK-009/task009-pytest-20260806.txt`: `7 passed`.
- `docs/evidence/TASK-009/task009-pytest-final-20260806.txt`: `7 passed`.
- `docs/evidence/TASK-009/task009-mock-tts-cli-20260806.txt`: Mock TTS returns deterministic bytes.
- `docs/evidence/TASK-009/task009-mock-tts-cli-final-20260806.txt`: Mock TTS returns deterministic bytes.
- `docs/evidence/TASK-009/task009-doubao-tts-cli-missing-credentials-20260806.txt`: real Doubao path returns `BLOCKED_PROVIDER_CREDENTIALS`.
- `docs/evidence/TASK-009/task009-doubao-tts-cli-missing-credentials-final-20260806.txt`: real Doubao path returns `BLOCKED_PROVIDER_CREDENTIALS`, process exit code `2`.
- `docs/evidence/TASK-009/task009-safe-config-summary-20260806.txt`: required credentials are `missing`, no values printed.
- `docs/evidence/TASK-009/task009-safe-config-summary-final-20260806.txt`: required credentials are `missing`, no values printed.
- `docs/evidence/TASK-009/task009-diff-check-20260806.txt`: `git diff --check` exit 0, with CRLF warning only.
- `docs/evidence/TASK-009/task009-repository-verify-20260806.txt`: repository verifier PASS.
- `docs/evidence/TASK-009/task009-secret-shape-scan-20260806.txt`: no API key/private-key/Bearer-token shape matches.
- `docs/evidence/TASK-009/task009-gateway-missing-credential-test-20260806.txt`: 8 tests passed, including Gateway `doubao` TTS missing-credential 503 behavior.
- `docs/evidence/TASK-009/task009-post-hardening-diff-check-20260806.txt`: `git diff --check` exit 0.
- `docs/evidence/TASK-009/task009-config-preflight-pytest-20260806.txt`: 9 tests passed, including redacted config status coverage.
- `docs/evidence/TASK-009/task009-doubao-tts-config-preflight-20260806.txt`: config preflight returns `BLOCKED_PROVIDER_CREDENTIALS` with missing/configured status only.
- `docs/evidence/TASK-009/task009-config-preflight-diff-check-20260806.txt`: `git diff --check` exit 0.
- `docs/evidence/TASK-009/task009-env-template-pytest-20260806.txt`: 9 tests passed after `.env.example` alignment.
- `docs/evidence/TASK-009/task009-env-template-preflight-20260806.txt`: Doubao preflight still returns `BLOCKED_PROVIDER_CREDENTIALS`.
- `docs/evidence/TASK-009/task009-env-template-secret-shape-scan-20260806.txt`: no API key/private-key/Bearer-token shape matches.
- `docs/evidence/TASK-009/task009-blocker-recheck-20260806.txt`: blocker recheck still returns `BLOCKED_PROVIDER_CREDENTIALS` for the three required TTS variables.
- `docs/evidence/TASK-009/task009-v3-pytest-20260806.txt`: 10 tests passed after V3 adapter update.
- `docs/evidence/TASK-009/task009-doubao-v3-config-preflight-20260806.txt`: external private env preflight returned configured app/access auth, speaker and resource ID; values were not printed.
- `docs/evidence/TASK-009/task009-doubao-v3-real-call-20260806.txt`: real Doubao TTS call returned audio/mpeg, 20589 bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`.
- `docs/evidence/TASK-009/task009-doubao-v3-ffprobe-20260806.txt`: ffprobe verified MP3, 24000 Hz, mono, duration `2.568000`, size `20589`.
- `docs/evidence/TASK-009/task009-v3-diff-check-20260806.txt`: `git diff --check` exit 0.
- `docs/evidence/TASK-009/task009-v3-secret-shape-scan-20260806.txt`: no API key/private-key/Bearer-token shape matches in changed/evidence files.
- `docs/evidence/TASK-009/task009-final-pytest-20260806.txt`: 10 tests passed in final verification.
- `docs/evidence/TASK-009/task009-final-diff-check-20260806.txt`: `git diff --check` exit 0 with CRLF warning for `PROJECT_STATE.md`.
- `docs/evidence/TASK-009/task009-final-repository-verify-20260806.txt`: repository verification PASS.
- `docs/evidence/TASK-009/task009-final-secret-shape-scan-20260806.txt`: no API key/private-key/Bearer-token shape matches in TASK-009 changed/evidence files.

## Real API Status

DONE for TASK-009 provider acceptance.

Real provider verification used the external private env file `E:\work\ai-kefu\.env.local` without printing values:

- `DOUBAO_TTS_APP_ID`: configured
- `DOUBAO_TTS_ACCESS_TOKEN`: configured
- `DOUBAO_TTS_API_KEY`: missing but not required because app/access auth is configured
- `DOUBAO_TTS_SPEAKER`: configured
- `DOUBAO_TTS_RESOURCE_ID`: configured

The generated test audio is stored under ignored `tmp\` and must not be committed.

## Reproduction

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3
ffprobe -hide_banner -v error -show_entries format=format_name,duration,size -show_entries stream=codec_name,codec_type,sample_rate,channels -of json tmp\doubao-tts-test.mp3
```
