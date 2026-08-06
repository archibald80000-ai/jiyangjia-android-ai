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
  - `third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth`: missing.
  - `third_party\LiveTalking\data\avatars\wav2lip256_avatar1\`: missing.
- Upstream README official asset sources were recorded:
  - Quark: `https://pan.quark.cn/s/83a750323ef0`
  - Google Drive: `https://drive.google.com/drive/folders/1FOC_MD6wdogyyX_7V1d4NDIO7P9NlSAJ?usp=sharing`
- Google Drive was unreachable from this machine, including a 2026-08-06 `gdown 6.1.0` retry with supported arguments.
- Quark public API probing on 2026-08-06 can list the official share folder and confirmed:
  - `wav2lip256_avatar1.zip` size `353735616`.
  - `s3fd.pth` size `89843225`.
  - `wav2lip256.pth` size `214670409`.
- Quark download URL probes against `/1/clouddrive/file/share/download` and `/1/clouddrive/file/download` returned HTTP 400 code `23018 download file size limit` without a logged-in/download-capable Quark session. No cookies, stoken, share_fid_token or download URLs were recorded.
- Quark Windows integrated package share `https://pan.quark.cn/s/a040bf5cb065` can be listed and contains:
  - `models/wav2lip.pth` size `214670409`.
  - `_internal/avatars/wav2lip/face_detection/detection/sfd/s3fd.pth` size `89843225`.
  - expanded `data/avatars/wav2lip256_avatar1`.
- The package avatar directory has 589 files totaling `106662008` bytes, largest file `319803` bytes.
- Small file download URL creation succeeds, but CLI GET of the returned signed URL returns HTTP `412 Precondition Failed`; large model/S3FD URL creation returns `23018`.
- Local clients exist at `D:\应用软件\KUAK\Quark\quark.exe` and `D:\应用软件\夸\QuarkCloudDrive\quark_cloud_drive.exe`; account/session storage was not opened and clients were not started.
- `gdown` was installed inside the ignored local Conda environment for the Google Drive attempt; `pip check` still passes.
- Follow-up exact local filename search found no `wav2lip256.pth`, `wav2lip.pth` or `wav2lip256_avatar1.tar.gz` in safe local roots.
- 2026-08-06 exact search in `Downloads`, `Desktop`, `Documents`, `E:\work\ai-kefu` and `E:\work\安卓大屏AI语音客服系统` also found no `s3fd.pth` or `wav2lip256_avatar1.zip`; `E:\work\积养家` was intentionally excluded.
- Follow-up public web search found repeated upstream Quark/Google Drive references but no verified official direct download URL.
- `scripts/start_livetalking.ps1` now performs Wav2Lip asset preflight and stops before model loading if required files are missing. Use `-SkipAssetCheck` only for diagnostic commands such as `--help`, not for claiming runtime readiness.

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
- `docs/evidence/TASK-003/quark-public-api-probe.txt`
- `docs/evidence/TASK-003/quark-public-api-folder-list.txt`
- `docs/evidence/TASK-003/quark-download-endpoint-error-details.txt`
- `docs/evidence/TASK-003/gdrive-official-source-retry-supported-args-20260806.txt`
- `docs/evidence/TASK-003/asset-unblock-downloads-exact-search-20260806.txt`
- `docs/evidence/TASK-003/start-script-asset-preflight-20260806.txt`
- `docs/evidence/TASK-003/start-script-help-skip-asset-check-20260806.txt`
- `docs/evidence/TASK-003/task003-asset-unblock-attempt-final-verification-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-public-list-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-targeted-asset-list-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-download-probe-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-avatar-tree-20260806.txt`
- `docs/evidence/TASK-003/quark-avatar-small-download-header-probe-20260806.txt`
- `docs/evidence/TASK-003/quark-download-url-shape-20260806.txt`
- `docs/evidence/TASK-003/quark-client-local-capability-20260806.txt`
- `docs/evidence/TASK-003/task003-official-package-attempt-final-verification-20260806.txt`

## Unblock action

Obtain the official assets from the upstream README sources or Windows integrated package and place them as:

```text
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\models\wav2lip.pth
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth
E:\work\ai-kefu\jiyangjia-ai\third_party\LiveTalking\data\avatars\wav2lip256_avatar1\
```

Record SHA-256 hashes before retrying service startup. The docs mention `wav2lip256_avatar1.tar.gz`, the live model share currently exposes `wav2lip256_avatar1.zip`, and the Windows integrated package exposes `data/avatars/wav2lip256_avatar1` already expanded. Any form is acceptable only if it produces the expected avatar folder. Do not advance to TASK-004 until TASK-003 has real LiveTalking startup and WebRTC/WHEP evidence.
