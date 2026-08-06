# TASK-008: Create FastAPI Gateway and unified Provider skeleton

- **Status:** DONE
- **Priority:** P0
- **Dependencies:** TASK-007
- **Branch:** `task/TASK-008-gateway-skeleton`
- **Owner:** Codex / assigned developer

## Objective

Create the FastAPI Gateway, required API surface and unified Provider skeleton for ASR, TTS, LLM, Embedding and lightweight RAG orchestration.

## Preconditions

- Android real-device validation is deferred to TASK-015 and does not block TASK-008.
- TASK-005 Android shell exists.

## Scope and allowed changes

- `gateway/`
- `tests/gateway/`
- `config/`
- `docs/evidence/TASK-008/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Real Doubao/Ark/OpenAI-compatible paid calls
- FAISS production index build
- Dify, LangFlow, Flowise or heavy admin UI
- Tencent Cloud deployment

## Detailed execution

1. Create a lightweight FastAPI service with configuration validation.
2. Implement required routes: `/health`, `/api/v1/health`, `/api/v1/dialogue/text`, `/api/v1/dialogue/audio`, `/api/v1/knowledge/index`, `/api/v1/knowledge/search`, `/api/v1/knowledge/status`, `/api/v1/audio/{audio_id}`, `/api/v1/client/config`.
3. Add ASR/TTS/LLM/Embedding Provider interfaces and deterministic Mock implementations.
4. Add SQLite-backed knowledge metadata/search skeleton with `approved`, `draft`, `rejected` status handling.
5. Add request IDs, sanitized logs and stable error models.
6. Add automated tests. Do not claim real provider, FAISS or deployment completion.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/gateway -q
```
```powershell
python -m gateway --help
```
```powershell
curl http://127.0.0.1:8080/api/v1/health
```

## Required deliverables

- [x] Gateway skeleton
- [x] Provider contracts
- [x] Required API endpoints
- [x] Tests and evidence report

## Acceptance criteria

- [x] Required health/dialogue/knowledge/audio/config endpoints
- [x] ASR/TTS/LLM/Embedding provider interfaces
- [x] Request IDs
- [x] Structured sanitized logs
- [x] SQLite knowledge skeleton with source/status fields
- [x] Tests and evidence baseline

## Stop / blocked conditions

- A destructive change, secret exposure, uncontrolled paid call or public network exposure would be required.
- A dependency is absent and cannot be safely installed inside the authorized scope.
- Real hardware/model/provider evidence is required but unavailable.
- Existing unrelated changes make safe staging impossible.

When blocked, complete all safe analysis, save sanitized evidence, set status to `BLOCKED` or `PARTIAL`, and state the exact unblock action.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Changed files and `git diff --stat`.
- Sanitized logs/screenshots where meaningful.
- Artifact paths and SHA-256 for APK/packages.
- Hardware/environment details for device/GPU claims.
- Failed cases, untested paths and cost-bearing calls.

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## TASK-008 Result

- FastAPI Gateway skeleton is implemented under `gateway/`.
- Required routes are implemented:
  - `GET /health`
  - `GET /api/v1/health`
  - `GET /api/v1/client/config`
  - `POST /api/v1/dialogue/text`
  - `POST /api/v1/dialogue/audio`
  - `POST /api/v1/knowledge/index`
  - `POST /api/v1/knowledge/search`
  - `GET /api/v1/knowledge/status`
  - `GET /api/v1/audio/{audio_id}`
- ASR/TTS/LLM/Embedding Provider interfaces and deterministic Mock providers are present.
- SQLite knowledge skeleton supports `approved`, `draft`, `rejected` and returns sources/request IDs.
- Verification passed:
  - `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway -q`: 4 passed.
  - `.\.venv\gateway-task008-py310\Scripts\python.exe -m gateway --help`: exit 0.
  - local HTTP checks on `127.0.0.1:18080`: health, client config, knowledge index/search, text dialogue and audio fetch passed.
  - `git diff --check`: exit 0.
  - `scripts/verify_repository.ps1`: PASS.
  - secret-shape scan: no API key/private-key/Bearer-token shape matches.
  - safe config summary: required real-provider credentials are `missing`; no values printed.
- Port `8080` was occupied locally; 18080 was used for verification.
- TASK-008 does not claim real Doubao ASR/TTS, real LLM, real Embedding API, FAISS production index or Android hardware success.
