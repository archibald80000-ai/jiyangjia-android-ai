# PROJECT_STATE

- **Project:** jiyangjia-ai-kiosk
- **State version:** 0.1.0
- **Updated:** 2026-08-05
- **Overall status:** PLANNED / BOOTSTRAP REQUIRED
- **Current authorized task:** TASK-000
- **Public repository target:** `archibald80000-ai/jiyangjia-ai-kiosk`

## Verified facts

- Android target system: Android 12.
- Existing cloud server: 8 CPU cores, 4 GB RAM, 10 Mbps, no GPU.
- LiveTalking upstream repository identified.
- Upstream lock target: `c963ad409c556918b7d23999bf87c47a7c05c932`.
- Local original knowledge materials exist outside this repository and are not yet curated.

## Not yet verified

- Android CPU architecture and screen resolution.
- USB Host / USB Audio Class support.
- Whether APK sideloading and ADB are enabled.
- Development machine CUDA/PyTorch compatibility.
- LiveTalking model weights and Avatar assets.
- WebRTC connectivity on the target network.
- Real Doubao ASR/TTS/LLM credentials and API behavior.
- Production domain, TLS certificate, firewall and TURN strategy.

## Current milestone

**M0 — Repository and execution discipline**

Exit criteria:

- Repository cloned to the fixed Windows path.
- Environment and Git status audited.
- LiveTalking upstream pulled at locked commit.
- No secrets tracked.
- TASK-000 report produced.

## Status vocabulary

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: authorized and actively being executed.
- `PARTIAL`: useful work completed but acceptance criteria not fully met.
- `BLOCKED`: cannot proceed without a concrete dependency.
- `DONE`: acceptance criteria passed with evidence.
- `DEFERRED`: intentionally postponed by product decision.
