# Handoff

## Current task

- Completed task: `TASK-002_LIVETALKING_ENVIRONMENT.md`
- Status: `DONE`
- Current branch: `task/TASK-002-livetalking-environment`
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
8. `docs/evidence/TASK-002/environment-matrix.md`

## What is verified

- `third_party/LiveTalking` is a real ignored Git checkout at locked commit `c963ad409c556918b7d23999bf87c47a7c05c932`.
- TASK-002 created a local ignored Conda runtime at `.venv\livetalking-task002`.
- Runtime Python is `3.12.13`.
- PyTorch stack is `torch 2.9.1+cu126`, `torchvision 0.24.1+cu126`, `torchaudio 2.9.1+cu126`.
- `pip install -r third_party\LiveTalking\requirements.txt` completed inside the isolated runtime.
- `pip check` returned `No broken requirements found.`
- Import checks passed for torch, torchvision, torchaudio, cv2, aiortc, aiohttp, aiohttp_cors, av, soundfile, librosa, transformers, diffusers, accelerate, edge_tts, dashscope, openai and selected LiveTalking server modules.
- PyTorch CUDA smoke test passed: CUDA available, one GPU detected, device name `NVIDIA GeForce RTX 4070 Laptop GPU`, CUDA tensor sum returned `4.0`.
- Global Python remained without torch after TASK-002.
- `.venv\livetalking-task002` is ignored via `.gitignore`.
- `scripts/start_livetalking.ps1 -ExtraArgs --help` successfully reached upstream `app.py --help`.

## What is not verified

- `models/wav2lip.pth` source, license, hash, placement or runtime usability.
- `data/avatars/wav2lip256_avatar1` source, license, hash, placement or runtime usability.
- LiveTalking service startup.
- WebRTC/WHEP media path, `/offer`, `/whep`, `/human`, `/humanaudio`, FPS or latency.
- Android APK, USB microphone, speaker routing, Doubao ASR/TTS/LLM and mini FAQ behavior.

## TASK-002 evidence

- `docs/evidence/TASK-002/environment-matrix.md`
- `docs/evidence/TASK-002/initial-environment-inventory.txt`
- `docs/evidence/TASK-002/conda-create-env.txt`
- `docs/evidence/TASK-002/pytorch-index-cu126.txt`
- `docs/evidence/TASK-002/pytorch-install-cu126.txt`
- `docs/evidence/TASK-002/livetalking-requirements-install.txt`
- `docs/evidence/TASK-002/import-and-device-checks.txt`
- `docs/evidence/TASK-002/livetalking-cli-help.txt`
- `docs/evidence/TASK-002/start-script-help-check.txt`
- `docs/evidence/TASK-002/pip-freeze.txt`
- `docs/evidence/TASK-002/pip-check.txt`
- `docs/evidence/TASK-002/conda-list.txt`
- `docs/evidence/TASK-002/conda-env-export.yaml`
- `docs/evidence/TASK-002/conda-explicit.txt`
- `docs/evidence/TASK-002/global-python-post-check.txt`
- `docs/evidence/TASK-002/task002-final-verification.txt`

## Next action

Start `TASK-003_WAV2LIP_WEBRTC_BASELINE.md` on a new task branch/session:

```powershell
git switch -c task/TASK-003-wav2lip-webrtc-baseline
```

TASK-003 should prepare real Wav2Lip model/avatar assets with source, license and hash evidence, then start LiveTalking and verify WebRTC/WHEP baseline behavior. Do not claim Wav2Lip, WebRTC, FPS or API success without runtime evidence.
