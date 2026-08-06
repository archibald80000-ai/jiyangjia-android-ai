# TASK-002 environment matrix

- Date: 2026-08-06
- Branch: `task/TASK-002-livetalking-environment`
- Status: `DONE`
- Local runtime path: `.venv\livetalking-task002`
- Upstream checkout: `third_party\LiveTalking`
- Locked upstream commit: `c963ad409c556918b7d23999bf87c47a7c05c932`

## Scope executed

- Inventoried global Python, Conda, FFmpeg, NVIDIA driver/CUDA and active Python PyTorch state.
- Created an ignored local Conda environment at `.venv\livetalking-task002`.
- Installed Python 3.12.13 and pip inside that local environment.
- Installed PyTorch `2.9.1+cu126`, torchvision `0.24.1+cu126` and torchaudio `2.9.1+cu126`.
- Installed upstream `third_party\LiveTalking\requirements.txt`.
- Ran import checks for core LiveTalking runtime dependencies and selected upstream modules.
- Ran a PyTorch CUDA tensor smoke test.
- Ran `pip check`, `pip freeze`, Conda list/export evidence and `app.py --help`.
- Added `scripts/start_livetalking.ps1` as a thin reproducible launcher for later tasks.

TASK-002 did not download model weights, prepare avatar assets, start the LiveTalking service, open WebRTC, run Wav2Lip inference or call real provider APIs.

## Environment choice

The global `python` command resolves to `D:\python311\python.exe` but reports Python `3.14.0`, and the global environment has no PyTorch. Upstream recommends Python 3.10+ and shows a Python 3.12 Conda setup, so TASK-002 uses a local Conda prefix under `.venv\livetalking-task002`.

The NVIDIA driver reports CUDA `12.7`. Upstream README shows PyTorch `2.9.1` with `cu128` as an example and says to choose the corresponding PyTorch build when CUDA is not 12.8. The PyTorch CUDA 12.6 index exposes `torch 2.9.1+cu126`, so TASK-002 keeps the upstream torch version while selecting a CUDA wheel that is under the reported driver capability.

## Matrix

| Component | Result | Evidence |
|---|---|---|
| Global Python | `Python 3.14.0`, executable `D:\python311\python.exe`; no global torch after setup | `initial-environment-inventory.txt`, `global-python-post-check.txt` |
| Conda | `conda 26.1.1` | `initial-environment-inventory.txt` |
| FFmpeg | `8.1-essentials_build-www.gyan.dev` | `initial-environment-inventory.txt` |
| GPU driver | NVIDIA driver `566.07`, reported CUDA `12.7` | `initial-environment-inventory.txt` |
| GPU device | `NVIDIA GeForce RTX 4070 Laptop GPU`, 8188 MiB reported by `nvidia-smi` | `initial-environment-inventory.txt` |
| Local runtime | `.venv\livetalking-task002`, Python `3.12.13`, pip `26.1.2` | `conda-create-env.txt`, `conda-list.txt` |
| PyTorch | `torch 2.9.1+cu126`, CUDA runtime `12.6` | `pytorch-install-cu126.txt`, `import-and-device-checks.txt` |
| PyTorch CUDA smoke | `torch.cuda.is_available() == true`; CUDA tensor sum returned `4.0` | `import-and-device-checks.txt` |
| LiveTalking requirements | `pip install -r third_party\LiveTalking\requirements.txt` exit 0 | `livetalking-requirements-install.txt` |
| Dependency consistency | `pip check` returned `No broken requirements found.` | `pip-check.txt` |
| Runtime imports | torch/torchvision/torchaudio/cv2/aiortc/aiohttp/av/soundfile/librosa/transformers/diffusers/accelerate and key LiveTalking server modules imported | `import-and-device-checks.txt` |
| LiveTalking CLI parser | `app.py --help` exit 0 | `livetalking-cli-help.txt` |

## Reproducible commands

```powershell
conda create --prefix .venv\livetalking-task002 python=3.12 pip -y
conda run -p .venv\livetalking-task002 python -m pip install torch==2.9.1+cu126 torchvision==0.24.1+cu126 torchaudio==2.9.1+cu126 --index-url https://download.pytorch.org/whl/cu126
conda run -p .venv\livetalking-task002 python -m pip install -r third_party\LiveTalking\requirements.txt
conda run -p .venv\livetalking-task002 python -m pip check
```

Supporting lock/evidence files:

- `conda-env-export.yaml`
- `conda-explicit.txt`
- `conda-list.txt`
- `pip-freeze.txt`

## Readiness and blockers

Ready for TASK-003:

- Local isolated Python runtime exists.
- PyTorch can see and use the local NVIDIA GPU at a tensor-smoke-test level.
- LiveTalking's core Python dependencies install and import.
- A launcher exists at `scripts/start_livetalking.ps1`.

Not ready / not claimed:

- Wav2Lip model weight `models/wav2lip.pth` has not been downloaded, hashed or licensed.
- Avatar folder `data/avatars/wav2lip256_avatar1` has not been downloaded, hashed or licensed.
- LiveTalking service startup and WebRTC/WHEP media path have not been tested.
- No FPS, latency, `/offer`, `/whep`, `/human` or `/humanaudio` success is claimed.

## Rollback

To remove the local runtime created by TASK-002, delete only `.venv\livetalking-task002`. Do not delete `third_party\LiveTalking`, model/avatar assets, unrelated virtual environments or user source materials.
