# TASK-002: Create an isolated, reproducible LiveTalking runtime environment

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-001
- **Branch:** `task/TASK-002-livetalking-environment`
- **Owner:** Codex / assigned developer

## Objective

Create an isolated, reproducible LiveTalking runtime environment.

## Preconditions

- TASK-001 is DONE
- Locked upstream exists

## Scope and allowed changes

- Local ignored runtime environment
- `scripts/start_livetalking.ps1 if needed`
- `docs/evidence/TASK-002/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Model success claim without weights/GPU

## Detailed execution

1. Inventory Python, Conda/venv, FFmpeg, NVIDIA driver, CUDA and installed PyTorch without changing global packages.
2. Choose one isolated environment compatible with the actual machine and upstream requirements; record the rationale.
3. Install the minimum upstream dependencies in that isolated environment with captured versions.
4. Run import and device checks. If GPU/CUDA is missing, mark the rendering path BLOCKED but finish CPU-independent setup evidence.
5. Do not download every model or silently upgrade system-wide CUDA/driver.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python --version
```
```powershell
conda --version
```
```powershell
ffmpeg -version
```
```powershell
nvidia-smi
```
```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```
```powershell
python -m pip freeze
```

## Required deliverables

- [ ] docs/evidence/TASK-002/environment-matrix.md
- [ ] Reproducible environment commands/lock
- [ ] Accurate GPU/CUDA blocker or readiness result

## Acceptance criteria

- [ ] Python/FFmpeg/GPU/CUDA/PyTorch matrix recorded
- [ ] Isolated environment created
- [ ] Dependency install command and failures documented
- [ ] No global Python damage

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
