# TASK-000: Bootstrap repository and audit the local environment

- **Status:** PARTIAL
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

- [x] docs/evidence/TASK-000/environment-audit.md
- [x] Clean/understood Git state
- [x] Updated project state and handoff

## Acceptance criteria

- [x] Repository cloned into the fixed Windows path
- [x] Secret protections verified
- [x] Tool/Git/environment audit documented
- [ ] Upstream bootstrap command verified without downloading weights

## TASK-000 result on 2026-08-06

Status is `PARTIAL`.

Evidence:

- `docs/evidence/TASK-000/environment-audit.md`
- `docs/evidence/TASK-000/check-prerequisites.txt`
- `docs/evidence/TASK-000/verify-repository.txt`
- `docs/evidence/TASK-000/secret-and-config-checks.txt`
- `docs/evidence/TASK-000/yaml-validation.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking.txt`
- `docs/evidence/TASK-000/github-network-diagnostic.txt`
- `docs/evidence/TASK-000/retry-github-network.txt`
- `docs/evidence/TASK-000/retry-git-http11.txt`
- `docs/evidence/TASK-000/retry-git-http11-second.txt`
- `docs/evidence/TASK-000/retry-gh-api.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking-http11.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking-wrapper-http11-bypass.txt`
- `docs/evidence/TASK-000/manual-clone-http11.txt`
- `docs/evidence/TASK-000/manual-init-fetch-http11.txt`
- `docs/evidence/TASK-000/github-archive-head-check.txt`
- `docs/evidence/TASK-000/cleanup-invalid-livetalking-checkout.txt`
- `docs/evidence/TASK-000/post-retry-verification.txt`

Summary:

- Fixed path and branch were verified.
- Repository structure verification passed.
- `.env.local` is ignored and absent; values were not read.
- Sensitive/model/audio/database tracked filename scans passed.
- JSON/YAML example validation passed.
- Prerequisite audit found Git, Python, Conda, FFmpeg, NVIDIA driver/CUDA via `nvidia-smi`, Java and GitHub CLI.
- ADB and Gradle are missing from PATH.
- PyTorch is not installed in the active Python environment.
- LiveTalking bootstrap failed because GitHub Git clone/fetch access to `https://github.com/lipku/LiveTalking.git` failed.
- `git -c http.version=HTTP/1.1 ls-remote` succeeded once and returned the locked commit, but later clone/fetch attempts with HTTP/1.1 still failed.
- GitHub API and locked-commit archive HEAD checks were reachable; archive was not used as a Git checkout replacement.
- A task-created invalid `third_party/LiveTalking` directory from manual `git init` was removed after path verification.

Next unblock action:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```

Run this only after GitHub Git clone/fetch access is fixed. Do not start TASK-001 until the locked checkout succeeds or an approved alternate retrieval path is documented.

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
