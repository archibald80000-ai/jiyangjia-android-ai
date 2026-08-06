# TASK-008: Create the lightweight gateway and common contracts

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-007
- **Branch:** `task/TASK-008-gateway-skeleton`
- **Owner:** Codex / assigned developer

## Objective

Create the lightweight gateway and common contracts.

## Preconditions

- TASK-007 is DONE or explicitly PARTIAL with a stable Android audio contract

## Scope and allowed changes

- `gateway/`
- `tests/gateway/`
- `config/`
- `docs/evidence/TASK-008/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Vector DB
- Heavy admin UI

## Detailed execution

1. Create a lightweight FastAPI service in an isolated Python project with configuration validation.
2. Implement health, sessions, client config/status and provider interface skeletons.
3. Add request IDs, structured sanitized logging and stable error models.
4. Use SQLite for development unless a task-specific ADR approves another database.
5. Add tests and measure idle process memory. Do not add document parsing/vector DB/admin UI.

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

- [ ] Gateway skeleton
- [ ] Provider contracts
- [ ] Tests and resource report

## Acceptance criteria

- [ ] Health/session/config/status endpoints
- [ ] Provider interfaces
- [ ] Request IDs
- [ ] Structured sanitized logs
- [ ] Tests and resource baseline

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

- [ ] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [ ] Add evidence links/results to this task.
- [ ] Update `PROJECT_STATE.md`.
- [ ] Update `memory/CURRENT_STATE.md`.
- [ ] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [ ] Recommend exactly one next task.
