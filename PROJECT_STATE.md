# PROJECT_STATE

- **Project:** jiyangjia-android-ai
- **State version:** 0.1.0
- **Updated:** 2026-08-06
- **Overall status:** PARTIAL / BOOTSTRAP BLOCKED
- **Current authorized task:** TASK-000
- **Public repository target:** `archibald80000-ai/jiyangjia-android-ai`

## Verified facts

- Android target system: Android 12.
- Existing cloud server: 8 CPU cores, 4 GB RAM, 10 Mbps, no GPU.
- LiveTalking upstream repository identified.
- Upstream lock target: `c963ad409c556918b7d23999bf87c47a7c05c932`.
- Local original knowledge materials exist outside this repository and are not yet curated.
- Local synchronized workspace is present at `E:\work\ai-kefu\jiyangjia-ai`.
- Repository structure verification passed with `scripts/verify_repository.ps1`.
- Project identity has been aligned to `archibald80000-ai/jiyangjia-android-ai`.
- TASK-000 ran on branch `task/TASK-000-project-bootstrap`.
- `.env.local` is ignored and was absent during the audit; values were not read.
- No tracked `.env`, private key, APK, model, audio or database file matched the TASK-000 scans.
- JSON/YAML example validation passed.
- Local tools found: Git, Python, Conda, FFmpeg, NVIDIA driver/CUDA via `nvidia-smi`, Java and GitHub CLI.

## Not yet verified

- Android CPU architecture and screen resolution.
- USB Host / USB Audio Class support.
- Whether APK sideloading and ADB are enabled.
- Development machine CUDA/PyTorch compatibility.
- Android SDK/ADB and Gradle availability.
- LiveTalking model weights and Avatar assets.
- LiveTalking locked checkout; GitHub Git clone/fetch access failed during TASK-000.
- WebRTC connectivity on the target network.
- Real Doubao ASR/TTS/LLM credentials and API behavior.
- Production domain, TLS certificate, firewall and TURN strategy.
- Whether the expanded local framework should replace the current GitHub `main` content or be published through a review branch.

## Current milestone

**M0 — Repository and execution discipline**

Exit criteria:

- Repository cloned to the fixed Windows path.
- Environment and Git status audited.
- LiveTalking upstream pulled at locked commit.
- No secrets tracked.
- TASK-000 report produced.

Current evidence:

- `docs/evidence/2026-08-06-local-sync-audit.md`
- `docs/evidence/TASK-000/environment-audit.md`

Current blocker:

- `powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1` failed because GitHub Git clone/fetch access to `https://github.com/lipku/LiveTalking.git` failed. A later `git -c http.version=HTTP/1.1 ls-remote` succeeded once and returned `c963ad409c556918b7d23999bf87c47a7c05c932`, but clone/fetch still failed. GitHub API and locked-commit archive HEAD checks were reachable; archive was not used as a checkout replacement. `third_party/LiveTalking` does not exist.

Next action:

- Resolve GitHub Git clone/fetch access and rerun TASK-000 bootstrap. Do not advance to TASK-001 until the locked checkout succeeds or a documented alternate upstream retrieval path is approved.

## Status vocabulary

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: authorized and actively being executed.
- `PARTIAL`: useful work completed but acceptance criteria not fully met.
- `BLOCKED`: cannot proceed without a concrete dependency.
- `DONE`: acceptance criteria passed with evidence.
- `DEFERRED`: intentionally postponed by product decision.
