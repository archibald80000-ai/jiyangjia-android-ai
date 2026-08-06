# TASK-003 Wav2Lip WebRTC baseline

- Date: 2026-08-06
- Branch: `task/TASK-003-wav2lip-webrtc-baseline`
- Status: `BLOCKED`
- Upstream checkout: `third_party\LiveTalking`
- Locked upstream commit: `c963ad409c556918b7d23999bf87c47a7c05c932`

## Objective

Run the first Wav2Lip WebRTC/WHEP baseline with real model and avatar assets.

## Result

TASK-003 is blocked before service startup because the required Wav2Lip model weight, S3FD detector weight and avatar package are missing locally, and the official online asset sources could not be automatically downloaded in this environment.

No LiveTalking service startup, WebRTC/WHEP stream, FPS, `/offer`, `/whep`, `/human` or `/humanaudio` success is claimed.

## Verified local state

Required path checks:

| Required item | Expected path | Current result |
|---|---|---|
| Wav2Lip model | `third_party\LiveTalking\models\wav2lip.pth` | Missing |
| S3FD detector | `third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth` | Missing |
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
- Public Quark API probing on 2026-08-06 obtained a share token and enumerated the official `wav2lip` folder without recording cookies, stoken or share file tokens.
- The Quark share currently lists `wav2lip256_avatar1.zip` (`353735616` bytes), `s3fd.pth` (`89843225` bytes) and `wav2lip256.pth` (`214670409` bytes).
- Quark download URL creation through `/1/clouddrive/file/share/download` and `/1/clouddrive/file/download` returned HTTP 400 code `23018` (`download file size limit`) for the listed files without a logged-in/download-capable Quark session.
- A Google Drive retry with installed `gdown 6.1.0` and supported arguments still timed out connecting to `drive.google.com:443`.
- Docker image export was considered but `docker` is not installed on this machine.
- `scripts/start_livetalking.ps1` now performs a Wav2Lip asset preflight and stops before model loading when the required files are absent.
- The official README Windows integrated package share (`https://pan.quark.cn/s/a040bf5cb065`) was probed on 2026-08-06. It is listable through Quark public share APIs and contains `models/wav2lip.pth`, `_internal/avatars/wav2lip/face_detection/detection/sfd/s3fd.pth` and `data/avatars/wav2lip256_avatar1`.
- In that Windows package share, small file download URL creation succeeds, but direct CLI GET of the returned URL returns HTTP 412. Large `wav2lip.pth` and `s3fd.pth` download URL creation still returns `23018 download file size limit`.
- The Windows package avatar directory contains 589 files totaling `106662008` bytes; each avatar file is small enough in principle, but the returned signed URL still failed under CLI header variants tested so the avatar was not downloaded.
- Local Quark and QuarkCloudDrive clients are installed, but no client was started and no login/session storage was read.
- Candidate local download directories (`Downloads`, `downloadtemp`, `D:\BaiduNetdiskDownload`, `D:\QLDownload`, Quark install roots and similar) were searched by exact filename on 2026-08-06; no existing local copy of `wav2lip.pth`, `wav2lip256.pth`, `s3fd.pth`, `wav2lip256_avatar1.zip`, `wav2lip256_avatar1.tar.gz` or `coords.pkl` was found.
- `scripts/start_livetalking.ps1` now supports an explicit local preparation mode: `-PrepareAssets -AssetSourcePath <downloaded_official_source>`. It does not download assets or read Quark/browser login storage; it only copies from a user-provided local directory and emits SHA-256 evidence.

Evidence:

- `initial-asset-and-env-check.txt`
- `gdown-install.txt`
- `gdrive-download.txt`
- `gdrive-download-retry.txt`
- `asset-source-reachability.txt`
- `quark-page-probe.txt`
- `asset-unblock-followup-local-search.txt`
- `asset-unblock-followup-web-search.md`
- `quark-public-api-probe.txt`
- `quark-public-api-folder-list.txt`
- `quark-page-script-urls.txt`
- `quark-share-download-url-probe.txt`
- `quark-download-endpoint-error-details.txt`
- `quark-desktop-ua-download-url-probe.txt`
- `quark-file-download-desktop-ua-probe.txt`
- `quark-batch-download-probe.txt`
- `gdrive-official-source-retry-20260806.txt`
- `gdrive-official-source-retry-supported-args-20260806.txt`
- `asset-unblock-downloads-exact-search-20260806.txt`
- `start-script-asset-preflight-20260806.txt`
- `start-script-help-skip-asset-check-20260806.txt`
- `task003-asset-unblock-attempt-final-verification-20260806.txt`
- `quark-windows-package-public-list-20260806.txt`
- `quark-windows-package-targeted-asset-list-20260806.txt`
- `quark-windows-package-download-probe-20260806.txt`
- `quark-windows-package-avatar-tree-20260806.txt`
- `quark-avatar-small-download-header-probe-20260806.txt`
- `quark-download-url-shape-20260806.txt`
- `quark-client-local-capability-20260806.txt`
- `task003-official-package-attempt-final-verification-20260806.txt`
- `asset-unblock-quark-download-dir-search-20260806.txt`
- `start-script-prepare-assets-mode-verification-20260806.txt`
- `task003-prepare-assets-mode-final-verification-20260806.txt`

## Manual unblock instructions

Use one of the official README/docs sources to obtain the exact files:

1. Download `wav2lip256.pth`.
2. Download `s3fd.pth`.
3. Download the `wav2lip256_avatar1` archive. The documentation says `wav2lip256_avatar1.tar.gz`; the live Quark listing observed on 2026-08-06 exposes `wav2lip256_avatar1.zip`.
4. Copy and rename the model:

```powershell
Copy-Item "<download_dir>\wav2lip256.pth" "E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\models\wav2lip.pth"
```

5. Copy the S3FD detector:

```powershell
Copy-Item "<download_dir>\s3fd.pth" "E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth"
```

6. Extract the avatar archive so this directory exists:

```text
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\data\avatars\wav2lip256_avatar1\
```

7. Record hashes before retrying TASK-003:

```powershell
Get-FileHash "third_party\LiveTalking\models\wav2lip.pth" -Algorithm SHA256
Get-FileHash "third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth" -Algorithm SHA256
Get-ChildItem "third_party\LiveTalking\data\avatars\wav2lip256_avatar1" -Recurse -File |
  Get-FileHash -Algorithm SHA256 |
  Sort-Object Path
```

8. Confirm the assets are non-zero and ignored by Git:

```powershell
Get-Item "third_party\LiveTalking\models\wav2lip.pth"
Get-Item "third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth"
Get-ChildItem "third_party\LiveTalking\data\avatars\wav2lip256_avatar1" -Recurse -File |
  Measure-Object -Property Length -Sum
git check-ignore -v third_party\LiveTalking\models\wav2lip.pth
git check-ignore -v third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth
git check-ignore -v third_party\LiveTalking\data\avatars\wav2lip256_avatar1
```

9. Retry service startup only after the above evidence exists:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_livetalking.ps1
```

## Stop decision

TASK-003 stops here by design. Starting LiveTalking without `models\wav2lip.pth`, `avatars\wav2lip\face_detection\detection\sfd\s3fd.pth` and `data\avatars\wav2lip256_avatar1` would only create a predictable failure and could be mistaken for real runtime evidence. The next action is to provide/download the official assets and rerun TASK-003 from the asset verification step.

## Follow-up on 2026-08-06

Additional exact local filename search checked `E:\work\ai-kefu`, `Downloads`, `Documents` and `Desktop` for `wav2lip256.pth`, `wav2lip.pth` and `wav2lip256_avatar1.tar.gz`; no matching assets were found. The raw business source path `E:\work\积养家` was not scanned.

Additional public web search found only repeated references to the same upstream Quark and Google Drive sources, not a verified official direct download URL. TASK-003 therefore remains blocked.

## Additional unblock attempt on 2026-08-06

Quark public API probing improved the blocker but did not fully unblock it:

- `sharepage/token` returned `code=0`.
- `sharepage/detail` listed the official folder and confirmed the three needed files by name and size.
- Download URL endpoints returned `23018 download file size limit` without a logged-in/download-capable Quark session.
- No explicit Quark auth environment variables were configured in the current process.
- Exact filename search in `Downloads`, `Desktop`, `Documents`, `E:\work\ai-kefu` and `E:\work\安卓大屏AI语音客服系统` found no local copy of the assets; `E:\work\积养家` was intentionally excluded.

The launcher was hardened so future retries fail early with exact missing asset paths instead of reaching a misleading runtime failure.

## Additional official package attempt on 2026-08-06

The README Windows integrated package is a better official fallback source than the raw model share because it exposes the already-renamed model and the expanded avatar directory:

- `models/wav2lip.pth`: found, `214670409` bytes.
- `_internal/avatars/wav2lip/face_detection/detection/sfd/s3fd.pth`: found, `89843225` bytes.
- `data/avatars/wav2lip256_avatar1`: found as an expanded directory.
- `data/avatars/wav2lip256_avatar1` contains 589 files, total `106662008` bytes, largest file `319803` bytes.

However, this still did not unblock runtime:

- Large model/S3FD download URL creation returns Quark code `23018`.
- Small file download URL creation succeeds, but direct CLI download of the signed URL returns HTTP `412 Precondition Failed` even with browser user-agent, referer and range header variants.
- The local Quark clients exist at `D:\应用软件\KUAK\Quark\quark.exe` and `D:\应用软件\夸\QuarkCloudDrive\quark_cloud_drive.exe`, but automated use of account/session state was not attempted.

The practical unblock path is now more precise: use the installed QuarkCloudDrive client or browser UI with an authorized logged-in account to download/transfer the official Windows package or the three listed assets, then place and hash the files under the ignored LiveTalking paths.

After that download is present locally, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_livetalking.ps1 `
  -PrepareAssets `
  -AssetSourcePath "<downloaded_official_source>"
```

The source can be either the official Windows package root containing `models`, `_internal` and `data`, or a local folder containing `wav2lip.pth`/`wav2lip256.pth`, `s3fd.pth` and the expanded `wav2lip256_avatar1` directory. Use `-OverwriteAssets` only after manually confirming the source.
