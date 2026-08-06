# Handoff

## Current task

- Current task: `TASK-003_WAV2LIP_WEBRTC_BASELINE.md`
- Status: `BLOCKED`
- Current branch: `task/TASK-003-wav2lip-webrtc-baseline`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; not scanned or modified)

## Read first

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `PROJECT_STATE.md`
5. `docs/22_DELIVERY_BLUEPRINT.md`
6. `docs/03_LIVETALKING_SCOPE.md`
7. `tasks/TASK-003_WAV2LIP_WEBRTC_BASELINE.md`
8. `docs/evidence/TASK-003/wav2lip-baseline.md`

## What is verified

- `third_party/LiveTalking` remains locked at commit `c963ad409c556918b7d23999bf87c47a7c05c932`.
- `.venv\livetalking-task002` still runs torch `2.9.1+cu126` with CUDA available.
- TASK-003 checked the expected asset paths:
  - `third_party\LiveTalking\models\wav2lip.pth`: missing.
  - `third_party\LiveTalking\data\avatars\wav2lip256_avatar1\`: missing.
- Upstream README official asset sources were recorded:
  - Quark: `https://pan.quark.cn/s/83a750323ef0`
  - Google Drive: `https://drive.google.com/drive/folders/1FOC_MD6wdogyyX_7V1d4NDIO7P9NlSAJ?usp=sharing`
- Google Drive was unreachable from this machine.
- Quark was reachable as a share web page, but non-interactive curl did not expose direct asset files.
- `gdown` was installed inside the ignored local Conda environment for the Google Drive attempt; `pip check` still passes.
- Follow-up exact local filename search found no `wav2lip256.pth`, `wav2lip.pth` or `wav2lip256_avatar1.tar.gz` in safe local roots.
- Follow-up public web search found repeated upstream Quark/Google Drive references but no verified official direct download URL.

## What is not verified

- Wav2Lip model source hash, license or runtime usability.
- Avatar source hash, license or runtime usability.
- LiveTalking service startup.
- WebRTC/WHEP media path, `/offer`, `/whep`, `/human`, `/humanaudio`, FPS or latency.
- Android APK, USB microphone, speaker routing, Doubao ASR/TTS/LLM and mini FAQ behavior.

## TASK-003 evidence

- `docs/evidence/TASK-003/wav2lip-baseline.md`
- `docs/evidence/TASK-003/initial-asset-and-env-check.txt`
- `docs/evidence/TASK-003/gdown-install.txt`
- `docs/evidence/TASK-003/gdrive-download.txt`
- `docs/evidence/TASK-003/gdrive-download-retry.txt`
- `docs/evidence/TASK-003/asset-source-reachability.txt`
- `docs/evidence/TASK-003/quark-page-probe.txt`
- `docs/evidence/TASK-003/asset-unblock-followup-local-search.txt`
- `docs/evidence/TASK-003/asset-unblock-followup-web-search.md`
- `docs/evidence/TASK-003/pip-check-after-gdown.txt`
- `docs/evidence/TASK-003/task003-final-verification.txt`
- `docs/evidence/TASK-003/task003-followup-final-verification.txt`
- `docs/evidence/TASK-003/task003-third-blocked-audit.txt`

## Unblock action

Obtain the official assets from the upstream README sources and place them as:

```text
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\models\wav2lip.pth
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\data\avatars\wav2lip256_avatar1\
```

Record SHA-256 hashes before retrying service startup. Do not advance to TASK-004 until TASK-003 has real LiveTalking startup and WebRTC/WHEP evidence.
