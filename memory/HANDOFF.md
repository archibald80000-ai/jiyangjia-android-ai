# Handoff

## Current task

- Completed task: `TASK-000_PROJECT_BOOTSTRAP.md`
- Status: `DONE`
- Current branch: `task/TASK-000-project-bootstrap`
- Last commit before this handoff update: `408bda8`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; not scanned or modified)

## Read first

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `PROJECT_STATE.md`
5. `docs/22_DELIVERY_BLUEPRINT.md`
6. `tasks/TASK-001_LIVETALKING_UPSTREAM_AUDIT.md`
7. `docs/evidence/TASK-000/environment-audit.md`

## What is verified

- Repository path is `E:\work\ai-kefu\jiyangjia-ai`.
- TASK-000 ran on `task/TASK-000-project-bootstrap`.
- Repository structure check passed with `scripts/verify_repository.ps1`.
- `.env.local` is ignored and absent; values were not read.
- Tracked sensitive/model/audio/database filename scans passed.
- JSON/YAML validation passed for the required examples and task/config files.
- Delivery blueprint exists at `docs/22_DELIVERY_BLUEPRINT.md`.
- `third_party/LiveTalking` is a real Git checkout at locked commit `c963ad409c556918b7d23999bf87c47a7c05c932`.
- `third_party/LiveTalking` is ignored by the main repository via `.gitignore:33`.
- No model weights or avatar packages were downloaded by TASK-000.

## Environment facts

- Git: found, `2.52.0.windows.1`.
- Python: found, `3.14.0`.
- Conda: found, `26.1.1`.
- FFmpeg: found, `8.1`.
- NVIDIA driver/CUDA as reported by `nvidia-smi`: driver `566.07`, CUDA `12.7`.
- Java: found, `9.0.1`.
- GitHub CLI: found, `2.87.3`.
- ADB: missing from PATH.
- Gradle: missing from PATH.
- PyTorch: not installed in the active Python environment.
- No `origin` remote is configured for the main repository.

## Bootstrap note

Default Git smart-HTTP clone/fetch to GitHub failed in earlier attempts. The successful command used process-scoped Git config:

```powershell
$env:GIT_CONFIG_COUNT='1'
$env:GIT_CONFIG_KEY_0='http.version'
$env:GIT_CONFIG_VALUE_0='HTTP/1.1'
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
Remove-Item Env:\GIT_CONFIG_COUNT, Env:\GIT_CONFIG_KEY_0, Env:\GIT_CONFIG_VALUE_0 -ErrorAction SilentlyContinue
```

This did not modify global Git configuration.

## Evidence

- `docs/evidence/TASK-000/environment-audit.md`
- `docs/evidence/TASK-000/bootstrap-livetalking-env-config-http11.txt`
- `docs/evidence/TASK-000/locked-checkout-final.txt`
- `docs/evidence/TASK-000/third-party-ignore-check.txt`
- `docs/evidence/TASK-000/task000-done-final-verification.txt`
- `docs/evidence/TASK-000/post-retry-verification.txt`
- Earlier failed retry logs remain under `docs/evidence/TASK-000/` for troubleshooting history.

## Next action

Start `TASK-001_LIVETALKING_UPSTREAM_AUDIT.md` on a new task branch/session:

```powershell
git switch -c task/TASK-001-livetalking-upstream-audit
```

TASK-001 should audit the locked upstream source, remote, branch/detached state, relevant README/API/config/source files, licenses, extension points and risks. Do not install model weights, do not run Wav2Lip, and do not modify upstream source in TASK-001.
