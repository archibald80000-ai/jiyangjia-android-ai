# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-009_TTS_PROVIDERS.md`
- Previous task: `TASK-008_GATEWAY_SKELETON.md` is DONE locally.
- Current branch: `task/TASK-008-provider-gateway`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## What TASK-008 delivered

- FastAPI Gateway package under `gateway/`.
- Required API routes:
  - `GET /health`
  - `GET /api/v1/health`
  - `GET /api/v1/client/config`
  - `POST /api/v1/dialogue/text`
  - `POST /api/v1/dialogue/audio`
  - `POST /api/v1/knowledge/index`
  - `POST /api/v1/knowledge/search`
  - `GET /api/v1/knowledge/status`
  - `GET /api/v1/audio/{audio_id}`
- Provider interfaces and Mock implementations for ASR, TTS, LLM and Embedding.
- SQLite knowledge skeleton with `approved`, `draft`, `rejected`.
- Mock dialogue orchestration returns `request_id`, `sources`, subtitles and `audio_id`.

## Evidence

- `docs/evidence/TASK-008/gateway-skeleton.md`
- `docs/evidence/TASK-008/task008-pip-install-py310-20260806.txt`
- `docs/evidence/TASK-008/task008-pytest-20260806.txt`
- `docs/evidence/TASK-008/task008-python-module-help-20260806.txt`
- `docs/evidence/TASK-008/task008-local-server-18080-20260806.txt`
- `docs/evidence/TASK-008/task008-diff-check-final-20260806.txt`
- `docs/evidence/TASK-008/task008-repository-verify-final-20260806.txt`
- `docs/evidence/TASK-008/task008-secret-shape-scan-20260806.txt`
- `docs/evidence/TASK-008/task008-safe-config-summary-20260806.txt`

## Verified commands

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway -q`: 4 passed.
- `.\.venv\gateway-task008-py310\Scripts\python.exe -m gateway --help`: exit 0.
- Local HTTP verification used port `18080` because local port `8080` was occupied.

## Important limits

- TASK-008 is Mock-only for providers.
- Do not claim Doubao ASR, Doubao TTS, Doubao/Volcengine Ark LLM, OpenAI-compatible fallback or Embedding API are working yet.
- FAISS and document parsing are planned for TASK-012.
- Android hardware validation is deferred to TASK-015.
- No `.env.local` values were read or printed.
- Safe config summary reports `DOUBAO_TTS_KEY` and the other real-provider credentials as `missing`.

## Next action

Execute exactly one next task: `TASK-009_TTS_PROVIDERS.md`.

Before implementing real Doubao TTS:

- verify current official Doubao/Volcengine TTS API documentation;
- list required env vars by name only;
- if credentials are missing, mark `BLOCKED_PROVIDER_CREDENTIALS`;
- do not place keys in Android, source files, tests or logs.
