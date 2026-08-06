# TASK-000 environment audit

- Date: 2026-08-06
- Branch: `task/TASK-000-project-bootstrap`
- Workspace: `E:\work\ai-kefu\jiyangjia-ai`
- Status: `DONE`

## Scope executed

- Read required project entry, governance, memory, state, roadmap and task files.
- Inventoried repository structure and tracked files.
- Switched from `main` to `task/TASK-000-project-bootstrap`.
- Ran prerequisite, repository, secret, JSON/YAML and bootstrap checks.
- Added a delivery blueprint that connects architecture, task dependencies, evidence gates, rollback and long-term route.

## Command results

| Command | Result | Evidence |
|---|---|---|
| `Get-Location` | `E:\work\ai-kefu\jiyangjia-ai` | `git-and-location.txt` |
| `git status --short --branch --untracked-files=all` | Dirty working tree understood; branch is `task/TASK-000-project-bootstrap` | `git-and-location.txt` |
| `git remote -v` | No remote configured | `git-and-location.txt` |
| `powershell -ExecutionPolicy Bypass -File .\scripts\check_prerequisites.ps1` | Exit 0 | `check-prerequisites.txt` |
| `powershell -ExecutionPolicy Bypass -File .\scripts\verify_repository.ps1` | Exit 0, `Repository verification: PASS` | `verify-repository.txt` |
| `git check-ignore -v .env.local` | `.env.local` ignored by `.gitignore:3` | `secret-and-config-checks.txt` |
| `git ls-files` sensitive scan | No tracked `.env`, private key, APK, model, audio or database file matched | `secret-and-config-checks.txt`, `repository-inventory.txt` |
| `python -m json.tool config/upstream-lock.json` | Exit 0 | `secret-and-config-checks.txt` |
| `python -m json.tool PROJECT_MANIFEST.json` | Exit 0 | `secret-and-config-checks.txt` |
| `python -m json.tool knowledge-test/test_questions.example.json` | Exit 0 | `secret-and-config-checks.txt` |
| PyYAML validation for task/config/FAQ YAML | Exit 0 | `yaml-validation.txt` |
| `python -c "import torch; ..."` | `ModuleNotFoundError: No module named 'torch'` | `python-torch-check.txt` |
| `powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1` | Exit 1, GitHub clone connection reset | `bootstrap-livetalking.txt` |
| `git ls-remote https://github.com/lipku/LiveTalking.git HEAD` | Exit 128, GitHub HTTPS connection reset | `github-network-diagnostic.txt` |
| `git -c http.version=HTTP/1.1 ls-remote https://github.com/lipku/LiveTalking.git HEAD` | Succeeded once and returned the locked commit, then failed later during retry | `retry-git-http11.txt`, `retry-git-http11-second.txt` |
| `gh repo view lipku/LiveTalking --json name,defaultBranchRef` | Exit 0; GitHub API route reachable | `retry-gh-api.txt` |
| `Invoke-WebRequest -Method Head` for locked commit archive | HTTP 200; archive route reachable but not used as checkout replacement | `github-archive-head-check.txt` |
| Temporary HTTP/1.1 bootstrap wrapper | Failed; clone could not connect to `github.com:443` | `bootstrap-livetalking-wrapper-http11-bypass.txt` |
| Manual `git init` plus locked commit `fetch` | Failed; fetch could not connect to `github.com:443` | `manual-init-fetch-http11.txt` |
| Cleanup invalid checkout directory | Removed task-created invalid `third_party/LiveTalking` directory after path verification | `cleanup-invalid-livetalking-checkout.txt` |
| Post-retry repository verification | `verify_repository.ps1` passed; `git diff --check` passed; private IP scan had no matches | `post-retry-verification.txt` |
| Process-scoped Git HTTP/1.1 bootstrap | `scripts/bootstrap_livetalking.ps1` completed; locked checkout created at `c963ad409c556918b7d23999bf87c47a7c05c932`; no weights/avatar packages downloaded | `bootstrap-livetalking-env-config-http11.txt` |
| Locked checkout final check | `rev-parse HEAD` matched lock; status was detached `HEAD`; remote was `https://github.com/lipku/LiveTalking.git` | `locked-checkout-final.txt` |
| Main repo ignore check | `third_party/LiveTalking` matched `.gitignore:33` and is not tracked by the main repository | `third-party-ignore-check.txt` |
| Final TASK-000 verification | `verify_repository.ps1` passed; checkout HEAD matched lock; ignored checkout verified; `git diff --check` passed | `task000-done-final-verification.txt` |

## Tool availability

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
- `.env.local`: missing; values were not read or printed.

## Findings

- Repository structure verification passed.
- The current local repository has no `origin` remote.
- Existing uncommitted changes before this task aligned the project identity and path to `jiyangjia-android-ai` / `E:\work\ai-kefu\jiyangjia-ai`.
- `.codex/TASK_EXECUTION_PROMPT.md` still contained the previous project name/path and was corrected during this task.
- LiveTalking checkout exists at `third_party/LiveTalking` and is ignored by the main repository.

## Previous blocker and resolution

The upstream bootstrap gate initially failed because GitHub Git smart-HTTP clone/fetch access for `https://github.com/lipku/LiveTalking.git` failed repeatedly under the default Git HTTP behavior. TCP 443, GitHub API and locked-commit archive HEAD checks were reachable, and one HTTP/1.1 `ls-remote` succeeded.

The gate passed after running the existing bootstrap script with process-scoped Git config:

```powershell
$env:GIT_CONFIG_COUNT='1'
$env:GIT_CONFIG_KEY_0='http.version'
$env:GIT_CONFIG_VALUE_0='HTTP/1.1'
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```

This created a real Git checkout and did not change global Git configuration.

## Untested

- Android SDK/ADB/device access.
- Gradle or Android APK build.
- PyTorch/CUDA compatibility inside an isolated LiveTalking environment.
- LiveTalking model weights, avatar assets, service startup, WebRTC and FPS.
- Doubao or any paid provider API.
- USB microphone and speaker on the Android 12 device.

## Rollback

- Remove only the task-created `docs/evidence/TASK-000/` files and `docs/22_DELIVERY_BLUEPRINT.md` if this partial bootstrap must be reverted.
- Do not touch `E:\work\积养家`, `.env.local`, model files, avatar assets or unrelated local changes.

## Next unblock action

Run TASK-001 next:

```powershell
git switch -c task/TASK-001-livetalking-upstream-audit
```

Then audit the locked upstream source. Do not install model weights, do not run Wav2Lip, and do not edit upstream source in TASK-001.
