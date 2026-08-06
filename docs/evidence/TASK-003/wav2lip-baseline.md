# TASK-003 Wav2Lip WebRTC baseline

- Date: 2026-08-06
- Branch: `task/TASK-003-wav2lip-webrtc-baseline`
- Status: `BLOCKED`
- Upstream checkout: `third_party\LiveTalking`
- Locked upstream commit: `c963ad409c556918b7d23999bf87c47a7c05c932`

## Objective

Run the first Wav2Lip WebRTC/WHEP baseline with real model and avatar assets.

## Result

TASK-003 is blocked before service startup because the required Wav2Lip model weight and avatar package are missing locally, and the official online asset sources could not be automatically downloaded in this environment.

No LiveTalking service startup, WebRTC/WHEP stream, FPS, `/offer`, `/whep`, `/human` or `/humanaudio` success is claimed.

## Verified local state

Required path checks:

| Required item | Expected path | Current result |
|---|---|---|
| Wav2Lip model | `third_party\LiveTalking\models\wav2lip.pth` | Missing |
| Default avatar | `third_party\LiveTalking\data\avatars\wav2lip256_avatar1\` | Missing |

Existing directory contents:

- `third_party\LiveTalking\models\` only contains `put models here.txt`.
- `third_party\LiveTalking\data\avatars\` only contains `.gitkeep`.

Runtime readiness from TASK-002 remains valid:

- `.venv\livetalking-task002` exists and is ignored.
- `torch 2.9.1+cu126` imports.
- CUDA is available to PyTorch.
- GPU detected: `NVIDIA GeForce RTX 4070 Laptop GPU`.

## Official source references

The locked upstream README lists these asset sources and placement instructions:

- Quark: `https://pan.quark.cn/s/83a750323ef0`
- Google Drive: `https://drive.google.com/drive/folders/1FOC_MD6wdogyyX_7V1d4NDIO7P9NlSAJ?usp=sharing`
- Copy `wav2lip256.pth` to `models/` and rename it to `wav2lip.pth`.
- Extract `wav2lip256_avatar1.tar.gz` and copy the extracted `wav2lip256_avatar1` folder to `data/avatars/`.

## Download attempts

Automated attempts:

- Installed `gdown` inside the ignored local Conda environment.
- `gdown --folder` against the Google Drive folder failed because this machine could not connect to `drive.google.com:443`.
- `curl -I` to the Google Drive folder also failed to connect.
- `curl -I` to the Quark URL returned HTTP 200.
- `curl -L` to the Quark URL returned only the share web shell page, not direct asset files.

Evidence:

- `initial-asset-and-env-check.txt`
- `gdown-install.txt`
- `gdrive-download.txt`
- `gdrive-download-retry.txt`
- `asset-source-reachability.txt`
- `quark-page-probe.txt`
- `asset-unblock-followup-local-search.txt`
- `asset-unblock-followup-web-search.md`

## Manual unblock instructions

Use one of the official README sources to obtain the exact files:

1. Download `wav2lip256.pth`.
2. Download `wav2lip256_avatar1.tar.gz`.
3. Copy and rename the model:

```powershell
Copy-Item "<download_dir>\wav2lip256.pth" "E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\models\wav2lip.pth"
```

4. Extract the avatar archive so this directory exists:

```text
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\data\avatars\wav2lip256_avatar1\
```

5. Record hashes before retrying TASK-003:

```powershell
Get-FileHash "third_party\LiveTalking\models\wav2lip.pth" -Algorithm SHA256
Get-ChildItem "third_party\LiveTalking\data\avatars\wav2lip256_avatar1" -Recurse -File |
  Get-FileHash -Algorithm SHA256 |
  Sort-Object Path
```

6. Confirm the assets are non-zero and ignored by Git:

```powershell
Get-Item "third_party\LiveTalking\models\wav2lip.pth"
Get-ChildItem "third_party\LiveTalking\data\avatars\wav2lip256_avatar1" -Recurse -File |
  Measure-Object -Property Length -Sum
git check-ignore -v third_party\LiveTalking\models\wav2lip.pth
git check-ignore -v third_party\LiveTalking\data\avatars\wav2lip256_avatar1
```

7. Retry service startup only after the above evidence exists:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_livetalking.ps1
```

## Stop decision

TASK-003 stops here by design. Starting LiveTalking without `models\wav2lip.pth` and `data\avatars\wav2lip256_avatar1` would only create a predictable failure and could be mistaken for real runtime evidence. The next action is to provide/download the two official assets and rerun TASK-003 from the asset verification step.

## Follow-up on 2026-08-06

Additional exact local filename search checked `E:\work\ai-kefu`, `Downloads`, `Documents` and `Desktop` for `wav2lip256.pth`, `wav2lip.pth` and `wav2lip256_avatar1.tar.gz`; no matching assets were found. The raw business source path `E:\work\积养家` was not scanned.

Additional public web search found only repeated references to the same upstream Quark and Google Drive sources, not a verified official direct download URL. TASK-003 therefore remains blocked.
