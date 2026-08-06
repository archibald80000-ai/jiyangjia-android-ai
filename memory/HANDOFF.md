# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-011_LLM_ROUTER.md`
- Previous task: `TASK-010_ASR_PROVIDERS.md`
- Previous task status: `DONE`
- Current branch: `task/TASK-010-asr-providers`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## TASK-010 done

- `gateway.app.asr.DoubaoASRProvider` implements Doubao/Volcengine big-model WebSocket ASR.
- Gateway uses bounded file/bytes-to-WebSocket chunks; Android always-on streaming remains a non-goal.
- Non-WAV/PCM inputs are normalized with ffmpeg to 16 kHz mono PCM WAV before ASR.
- `scripts/test_asr_provider.py` supports `--env-file` so private env files can be used without copying them into the repository.
- `.env.example` contains placeholders for ASR endpoint, auth, resource ID, chunk size and timeout.
- Missing credential reporting remains sanitized and does not print values.

## TASK-010 evidence

- `docs/evidence/TASK-010/asr-provider.md`
- `docs/evidence/TASK-010/task010-doubao-asr-config-preflight-20260806.txt`
- `docs/evidence/TASK-010/task010-doubao-asr-real-call-mp3-normalized-20260806.txt`
- `docs/evidence/TASK-010/task010-doubao-asr-real-call-wav-20260806.txt`
- `docs/evidence/TASK-010/task010-doubao-asr-debug-response-shape-20260806.txt`
- `docs/evidence/TASK-010/task010-asr-wav-fixture-ffprobe-20260806.txt`
- `docs/evidence/TASK-010/task010-mock-asr-cli-20260806.txt`
- `docs/evidence/TASK-010/task010-pytest-final-20260806.txt`

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\asr tests\gateway tests\tts -q`: 16 passed.
- External private env preflight with `E:\work\ai-kefu\.env.local` returned `ok=true`; values were not printed.
- Real Doubao ASR call on generated TTS smoke audio succeeded after MP3-to-WAV normalization.
- Observed transcript: `您好，欢迎来到机养家。`
- Expected phrase: `您好，欢迎来到积养家。`
- Known quality issue: `积养家` was recognized as `机养家`; handle later with vocabulary/post-ASR correction or RAG grounding.
- Generated test audio and normalized WAV remain under ignored `tmp\` and were not committed.

## Not verified

- Android recording upload into real ASR on device.
- Doubao/Volcengine Ark LLM, OpenAI-compatible fallback LLM and Embedding API.
- Lightweight RAG ingestion/search with real embeddings.
- Android end-to-end voice loop and Android 12 real-device acceptance.

## Next action

Start exactly one next task: `TASK-011_LLM_ROUTER.md`.

Do not proceed to TASK-012 until TASK-011 is verified or explicitly waived.
