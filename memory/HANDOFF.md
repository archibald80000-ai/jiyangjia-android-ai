# Handoff

## Current task

- Task: `TASK-000_PROJECT_BOOTSTRAP.md`
- Status: `PARTIAL`
- Branch: `task/TASK-000-project-bootstrap`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; not scanned or modified)

## Read first

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `PROJECT_STATE.md`
5. `docs/22_DELIVERY_BLUEPRINT.md`
6. `tasks/TASK-000_PROJECT_BOOTSTRAP.md`
7. `docs/evidence/TASK-000/environment-audit.md`

## What is verified

- Repository path is `E:\work\ai-kefu\jiyangjia-ai`.
- Current branch is `task/TASK-000-project-bootstrap`.
- Repository structure check passed with `scripts/verify_repository.ps1`.
- `.env.local` is ignored and absent; values were not read.
- Tracked sensitive/model/audio/database filename scans passed.
- `config/upstream-lock.json`, `PROJECT_MANIFEST.json` and `knowledge-test/test_questions.example.json` are valid JSON.
- `tasks/index.yaml`, `config/project.example.yaml`, `config/providers.example.yaml` and `knowledge-test/faq_test.example.yaml` are valid YAML with PyYAML.
- Delivery blueprint exists at `docs/22_DELIVERY_BLUEPRINT.md`.

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
- No `origin` remote is configured.

## Blocker

LiveTalking bootstrap did not complete:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```

Result: GitHub Git clone of `https://github.com/lipku/LiveTalking.git` failed.

Follow-up diagnostic:

```powershell
git ls-remote https://github.com/lipku/LiveTalking.git HEAD
```

Initial result: failed with connection reset.

Additional retry facts:

- `Test-NetConnection github.com -Port 443` succeeded.
- `git -c http.version=HTTP/1.1 ls-remote https://github.com/lipku/LiveTalking.git HEAD` succeeded once and returned `c963ad409c556918b7d23999bf87c47a7c05c932`.
- Later HTTP/1.1 clone/fetch attempts still failed to connect to `github.com:443`.
- `gh repo view lipku/LiveTalking --json name,defaultBranchRef` succeeded.
- `Invoke-WebRequest -Method Head` for the locked commit archive returned HTTP 200, but archive was not used as checkout replacement.
- A task-created invalid `third_party/LiveTalking` directory from manual `git init` was removed after verifying it was inside the project path.
- `third_party/LiveTalking` does not exist.

## Evidence

- `docs/evidence/TASK-000/environment-audit.md`
- `docs/evidence/TASK-000/git-and-location.txt`
- `docs/evidence/TASK-000/check-prerequisites.txt`
- `docs/evidence/TASK-000/verify-repository.txt`
- `docs/evidence/TASK-000/secret-and-config-checks.txt`
- `docs/evidence/TASK-000/yaml-validation.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking.txt`
- `docs/evidence/TASK-000/github-network-diagnostic.txt`
- `docs/evidence/TASK-000/python-torch-check.txt`
- `docs/evidence/TASK-000/java-adb-gradle-detail.txt`
- `docs/evidence/TASK-000/retry-github-network.txt`
- `docs/evidence/TASK-000/retry-git-http11.txt`
- `docs/evidence/TASK-000/retry-git-http11-second.txt`
- `docs/evidence/TASK-000/retry-gh-api.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking-http11.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking-wrapper-http11.txt`
- `docs/evidence/TASK-000/bootstrap-livetalking-wrapper-http11-bypass.txt`
- `docs/evidence/TASK-000/manual-clone-http11.txt`
- `docs/evidence/TASK-000/manual-init-fetch-http11.txt`
- `docs/evidence/TASK-000/github-archive-head-check.txt`
- `docs/evidence/TASK-000/cleanup-invalid-livetalking-checkout.txt`
- `docs/evidence/TASK-000/post-retry-verification.txt`

## Next action

Resolve GitHub Git clone/fetch access, then rerun:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```

If the locked checkout succeeds, update TASK-000 to `DONE` and only then proceed to `TASK-001_LIVETALKING_UPSTREAM_AUDIT.md`.
