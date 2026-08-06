# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-009_TTS_PROVIDERS.md`
- Status: `PARTIAL / BLOCKED_PROVIDER_CREDENTIALS`
- Current branch: `task/TASK-009-tts-providers`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## What is done

- TASK-007 follow-up audio device change monitoring was committed as `f6e931d`.
- TASK-008 Gateway/Provider skeleton was committed as `58b6edb`.
- TASK-009 implemented:
  - `gateway.app.tts.DoubaoTTSConfig`
  - `gateway.app.tts.DoubaoTTSProvider`
  - missing credential error `BLOCKED_PROVIDER_CREDENTIALS`
  - CLI helper `scripts/test_tts_provider.py`
  - tests under `tests/tts/`
  - TTS integration notes under `integration/tts/README.md`

## TASK-009 evidence

- `docs/evidence/TASK-009/tts-provider.md`
- `docs/evidence/TASK-009/task009-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-mock-tts-cli-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-tts-cli-missing-credentials-20260806.txt`
- `docs/evidence/TASK-009/task009-safe-config-summary-20260806.txt`
- `docs/evidence/TASK-009/task009-pytest-final-20260806.txt`
- `docs/evidence/TASK-009/task009-mock-tts-cli-final-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-tts-cli-missing-credentials-final-20260806.txt`
- `docs/evidence/TASK-009/task009-secret-shape-scan-20260806.txt`
- `docs/evidence/TASK-009/task009-gateway-missing-credential-test-20260806.txt`
- `docs/evidence/TASK-009/task009-config-preflight-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-tts-config-preflight-20260806.txt`
- `docs/evidence/TASK-009/task009-env-template-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-env-template-preflight-20260806.txt`
- `docs/evidence/TASK-009/task009-env-template-secret-shape-scan-20260806.txt`

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\tts tests\gateway -q`: 9 passed.
- Mock TTS CLI returned deterministic bytes with SHA-256 `248253DDDE4121C7512AF5E387BAAEC4EE48C7530D0EAB16F03A31D5DBFC9427`.
- Real Doubao TTS CLI path returned `BLOCKED_PROVIDER_CREDENTIALS`.
- `.env.example` uses TASK-009 provider variable names and placeholders only.

## Not verified

- Real Doubao TTS audio generation.
- Android playback of real Doubao audio.
- Doubao ASR, LLM, Embedding and RAG tasks.

## Blocker

Required credentials are missing:

- `DOUBAO_TTS_APP_ID`
- `DOUBAO_TTS_ACCESS_TOKEN`
- `DOUBAO_TTS_VOICE_TYPE`

No `.env.local` values were read or printed.

## Next action

Configure the above variables in `.env.local` or the server environment, then rerun:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3
```

Do not claim TASK-009 DONE until a real Doubao TTS audio file is generated and checked.
