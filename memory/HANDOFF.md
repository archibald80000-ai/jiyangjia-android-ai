# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-010_ASR_PROVIDERS.md`
- Previous task: `TASK-009_TTS_PROVIDERS.md`
- Previous task status: `DONE`
- Current branch: `task/TASK-009-tts-providers`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## TASK-009 done

- `gateway.app.tts.DoubaoTTSProvider` now defaults to Doubao/Volcengine V3 unidirectional HTTP streaming synthesis.
- Legacy V1 HTTP endpoint compatibility remains for older configurations.
- `scripts/test_tts_provider.py` supports `--env-file` so private env files can be used without copying them into the repository.
- `.env.example` contains placeholders for `DOUBAO_TTS_APP_ID`, `DOUBAO_TTS_ACCESS_TOKEN`, `DOUBAO_TTS_API_KEY`, `DOUBAO_TTS_SPEAKER`, `DOUBAO_TTS_RESOURCE_ID`, V3 endpoint and audio parameters.
- Missing credential reporting remains sanitized and does not print values.

## TASK-009 evidence

- `docs/evidence/TASK-009/tts-provider.md`
- `docs/evidence/TASK-009/task009-v3-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-config-preflight-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-real-call-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-ffprobe-20260806.txt`
- `docs/evidence/TASK-009/task009-v3-diff-check-20260806.txt`
- `docs/evidence/TASK-009/task009-v3-secret-shape-scan-20260806.txt`
- `docs/evidence/TASK-009/task009-final-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-final-diff-check-20260806.txt`
- `docs/evidence/TASK-009/task009-final-repository-verify-20260806.txt`
- `docs/evidence/TASK-009/task009-final-secret-shape-scan-20260806.txt`

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\tts tests\gateway -q`: 10 passed.
- External private env preflight with `E:\work\ai-kefu\.env.local` returned `ok=true`; values were not printed.
- Real Doubao TTS call generated ignored `tmp\doubao-tts-test.mp3`: `audio/mpeg`, `20589` bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`.
- `ffprobe` verified MP3, 24000 Hz, mono, 2.568 seconds.
- Secret-shape scan over changed/evidence files returned no matches.

## Not verified

- Android playback of the generated Doubao MP3.
- Doubao ASR.
- Doubao/Volcengine Ark LLM, OpenAI-compatible fallback LLM and Embedding API.
- Lightweight RAG ingestion/search with real embeddings.
- Android end-to-end voice loop and Android 12 real-device acceptance.

## Next action

Start exactly one next task: `TASK-010_ASR_PROVIDERS.md`.

Do not proceed to TASK-011 until TASK-010 is verified or explicitly waived.
