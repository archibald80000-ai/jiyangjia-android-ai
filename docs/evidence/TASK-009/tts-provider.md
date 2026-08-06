# TASK-009 TTS Provider Evidence

Date: 2026-08-06

## Official Documentation Checked

Official Volcengine/Doubao documentation entry points checked on 2026-08-06:

- `https://www.volcengine.com/docs/6561/1257584` - speech synthesis HTTP API.
- `https://www.volcengine.com/docs/6561/97465` - TTS access and parameter documentation entry.

Implementation uses the conservative HTTP non-streaming shape recorded from official documentation signals:

- endpoint: `https://openspeech.bytedance.com/api/v1/tts`
- authorization header: `Bearer; <access_token>`
- app fields: `appid`, `token`, `cluster`
- audio fields: `voice_type`, `encoding`, `speed_ratio`, `volume_ratio`, `pitch_ratio`
- request fields: `reqid`, `text`, `text_type`, `operation=query`

## Implemented

- Added `DoubaoTTSConfig` and `DoubaoTTSProvider`.
- Added missing-credential error: `BLOCKED_PROVIDER_CREDENTIALS`.
- Added safe provider call error mapping.
- Added CLI test helper: `scripts/test_tts_provider.py`.
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

## Real API Status

PARTIAL / BLOCKED_PROVIDER_CREDENTIALS.

The real Doubao TTS adapter code exists, but no real provider success is claimed because required credentials are missing:

- `DOUBAO_TTS_APP_ID`
- `DOUBAO_TTS_ACCESS_TOKEN`
- `DOUBAO_TTS_VOICE_TYPE`

## Required Unblock Action

Provide the above variables in `.env.local` or the server environment, then rerun:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3
```
