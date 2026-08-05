# TASK-000: Bootstrap repository and audit the local environment

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** None
- **Branch:** `task/TASK-000-project-bootstrap`
- **Owner:** Codex / assigned developer

## Objective

Bootstrap repository and audit the local environment.

## Preconditions

- Framework files are present in the fixed directory
- No implementation task is authorized yet

## Scope and allowed changes

- Root metadata and documentation
- `docs/evidence/TASK-000/`
- `PROJECT_STATE.md`
- `memory/CURRENT_STATE.md`
- `memory/HANDOFF.md`
- `tasks/TASK-000_PROJECT_BOOTSTRAP.md`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Android implementation
- Paid API calls
- Knowledge ingestion

## Detailed execution

1. Confirm `Get-Location` exactly matches the fixed Windows path and inventory existing files before writing.
2. Run `git status --short --branch`, inspect remotes, default branch and untracked files; do not overwrite unrelated work.
3. Run `scripts/check_prerequisites.ps1` and save a sanitized report under `docs/evidence/TASK-000/`.
4. Confirm `.env.local` is ignored and only report whether it exists; never read or print values.
5. Use `git check-ignore -v .env.local` and `git ls-files` checks to prove secrets/model/audio files are not tracked.
6. Validate JSON/YAML examples and required files.
7. Update state and handoff with real environment facts and select TASK-001 only if all bootstrap gates pass.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
Get-Location
```
```powershell
git status --short --branch
```
```powershell
git remote -v
```
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_prerequisites.ps1
```
```powershell
git check-ignore -v .env.local
```
```powershell
git ls-files
```
```powershell
python -m json.tool config/upstream-lock.json
```

## Required deliverables

- [ ] docs/evidence/TASK-000/environment-audit.md
- [ ] Clean/understood Git state
- [ ] Updated project state and handoff

## Acceptance criteria

- [ ] Repository cloned into the fixed Windows path
- [ ] Secret protections verified
- [ ] Tool/Git/environment audit documented
- [ ] Upstream bootstrap command verified without downloading weights

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
