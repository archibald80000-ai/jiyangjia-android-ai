# PROJECT_STATE

- **Project:** jiyangjia-android-ai
- **State version:** 0.1.0
- **Updated:** 2026-08-06
- **Overall status:** BLOCKED ON TASK-003 ASSET DOWNLOAD
- **Current authorized task:** TASK-003 (blocked; do not advance to TASK-004)
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
- LiveTalking locked checkout exists at ignored `third_party/LiveTalking` with HEAD `c963ad409c556918b7d23999bf87c47a7c05c932`.
- TASK-001 upstream audit completed on branch `task/TASK-001-livetalking-upstream-audit`.
- Static audit confirms LiveTalking exposes `/offer`, `/whep`, `/human`, `/humanaudio`, `/interrupt_talk`, `/is_speaking`, `/record`, `/record/{sessionid}`, `/set_audiotype`, `/sse`, admin routes, avatar task routes and conditional `/api/asr` at the locked commit.
- TASK-001 did not modify the ignored upstream checkout.
- TASK-002 completed on branch `task/TASK-002-livetalking-environment`.
- Isolated local runtime exists at ignored `.venv\livetalking-task002` with Python `3.12.13`.
- Local runtime installed `torch 2.9.1+cu126`, `torchvision 0.24.1+cu126`, `torchaudio 2.9.1+cu126` and upstream LiveTalking requirements.
- PyTorch CUDA smoke test passed in the isolated runtime: CUDA available, one NVIDIA GPU detected, device name `NVIDIA GeForce RTX 4070 Laptop GPU`, tensor sum returned `4.0`.
- `pip check` passed inside the isolated runtime.
- Global Python remained unmodified for torch after TASK-002.
- `scripts/start_livetalking.ps1` exists as a thin launcher for the isolated environment.
- TASK-003 ran on branch `task/TASK-003-wav2lip-webrtc-baseline` and stopped before service startup because required Wav2Lip assets are missing.
- Official README asset sources were recorded: Quark `https://pan.quark.cn/s/83a750323ef0` and Google Drive `https://drive.google.com/drive/folders/1FOC_MD6wdogyyX_7V1d4NDIO7P9NlSAJ?usp=sharing`.
- Google Drive could not be reached from this machine; Quark returned a web shell page but no direct non-interactive asset download.
- TASK-003 follow-up exact local filename search found no existing copies of `wav2lip256.pth`, `wav2lip.pth` or `wav2lip256_avatar1.tar.gz` in safe local roots; `E:\work\积养家` was not scanned.
- TASK-003 follow-up public web search found repeated upstream Quark/Google Drive references but no verified official direct download URL.
- TASK-003 Quark public API probe on 2026-08-06 succeeded in listing the official `wav2lip` folder without recording cookies/tokens: `wav2lip256_avatar1.zip` (`353735616` bytes), `s3fd.pth` (`89843225` bytes) and `wav2lip256.pth` (`214670409` bytes).
- TASK-003 Quark download URL probes against `/1/clouddrive/file/share/download` and `/1/clouddrive/file/download` returned HTTP 400 code `23018 download file size limit` without a logged-in/download-capable Quark session.
- TASK-003 Google Drive retry with `gdown 6.1.0` and supported arguments still timed out connecting to `drive.google.com:443`.
- TASK-003 exact filename search in common download/work roots found no local copies of `wav2lip256.pth`, `wav2lip.pth`, `s3fd.pth`, `wav2lip256_avatar1.zip` or `wav2lip256_avatar1.tar.gz`; `E:\work\积养家` was not scanned.
- `scripts/start_livetalking.ps1` now performs a Wav2Lip asset preflight and stops before model loading when required assets are missing.
- TASK-003 official Windows integrated package share (`https://pan.quark.cn/s/a040bf5cb065`) can be listed and contains `models/wav2lip.pth`, `_internal/avatars/wav2lip/face_detection/detection/sfd/s3fd.pth` and expanded `data/avatars/wav2lip256_avatar1`.
- The Windows package avatar directory contains 589 files totaling `106662008` bytes, but signed small-file URLs returned HTTP `412` under CLI GET; large model/S3FD URLs still returned `23018`.
- Local Quark clients are installed at `D:\应用软件\KUAK\Quark\quark.exe` and `D:\应用软件\夸\QuarkCloudDrive\quark_cloud_drive.exe`; account/session storage was not read and the clients were not started.
- TASK-003 searched common local download and Quark candidate directories by exact filename on 2026-08-06 and found no existing local copies of the required Wav2Lip/S3FD/avatar assets.
- `scripts/start_livetalking.ps1` now has an explicit local asset preparation mode: `-PrepareAssets -AssetSourcePath <downloaded_official_source>`, which copies from a user-provided local official source and outputs SHA-256 evidence without downloading or reading login/session storage.
- TASK-003 follow-up metadata-only search on 2026-08-06 scanned selected non-sensitive local roots by exact official file sizes (`214670409`, `89843225`, `353735616`) and `wav2lip256_avatar1` directory structure; no candidate assets were found. `E:\work\积养家` was excluded.
- `scripts/inspect_livetalking_assets.ps1` verifies a user-downloaded official Wav2Lip source before preparation. It does not download assets, copy model files or read browser/Quark login storage, and default checks reject same-name dummy files with non-official model/S3FD sizes.
- TASK-003 installation scripts now match the observed official asset layouts: model-share layout with `wav2lip256.pth`, `s3fd.pth`, `wav2lip256_avatar1.zip`; and Windows integrated package layout with `models/wav2lip.pth`, `_internal/.../s3fd.pth`, and expanded `data/avatars/wav2lip256_avatar1`. `-PrepareAssets` can extract the official avatar zip before copying to ignored LiveTalking paths.

## Not yet verified

- Android CPU architecture and screen resolution.
- USB Host / USB Audio Class support.
- Whether APK sideloading and ADB are enabled.
- Android SDK/ADB and Gradle availability.
- LiveTalking model weights and Avatar assets. Required TASK-003 files are still absent: `third_party\LiveTalking\models\wav2lip.pth`, `third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth` and `third_party\LiveTalking\data\avatars\wav2lip256_avatar1\`.
- WebRTC connectivity on the target network.
- LiveTalking service startup and Wav2Lip runtime behavior.
- Real Doubao ASR/TTS/LLM credentials and API behavior.
- Production domain, TLS certificate, firewall and TURN strategy.
- Whether the expanded local framework should replace the current GitHub `main` content or be published through a review branch.

## Current milestone

**M1 — LiveTalking reproducible baseline**

Exit criteria:

- Locked upstream source audited and runtime requirements understood.
- Isolated LiveTalking environment created.
- Wav2Lip model/avatar assets prepared with source/license/hash records.
- WebRTC/WHEP and core LiveTalking API behavior verified with real local evidence.

Current evidence:

- `docs/evidence/2026-08-06-local-sync-audit.md`
- `docs/evidence/TASK-000/environment-audit.md`
- `docs/evidence/TASK-001/upstream-audit.md`
- `docs/evidence/TASK-002/environment-matrix.md`
- `docs/evidence/TASK-003/wav2lip-baseline.md`

Recent task results:

- DONE. `scripts/bootstrap_livetalking.ps1` completed with process-scoped Git config `http.version=HTTP/1.1`; `third_party/LiveTalking` is a real ignored Git checkout at `c963ad409c556918b7d23999bf87c47a7c05c932`. No model weights or avatar packages were downloaded.
- TASK-001 DONE. Upstream README/API/config/source/license were audited and summarized. Static endpoint and integration boundaries are recorded in `docs/evidence/TASK-001/upstream-audit.md` and `docs/03_LIVETALKING_SCOPE.md`. No service, model, WebRTC or provider runtime success is claimed.
- TASK-002 DONE. A local ignored Conda runtime was created at `.venv\livetalking-task002`; PyTorch CUDA and LiveTalking dependency import checks passed. No model, avatar, service startup, WebRTC or provider success is claimed.
- TASK-003 BLOCKED. Required Wav2Lip model/S3FD/avatar assets are missing. Quark model and Windows package shares can be listed, but unauthenticated large-file download URL creation is blocked by `23018 download file size limit`, small signed URLs return HTTP `412` through CLI GET, Google Drive still times out from this machine, and local filename/size/structure searches found no existing copy. Safe local inspection/preparation now supports the official zip and Windows package layouts after authorized download. No LiveTalking startup/WebRTC/FPS success is claimed.

Next action:

- Unblock TASK-003 by using an authorized QuarkCloudDrive/browser download or reachable Google Drive path to obtain official `wav2lip.pth`/`wav2lip256.pth`, `s3fd.pth` and `wav2lip256_avatar1`; run `scripts/inspect_livetalking_assets.ps1 -AssetSourcePath <downloaded_official_source>` first, then run `scripts/start_livetalking.ps1 -PrepareAssets -AssetSourcePath <downloaded_official_source>` to place and hash them before rerunning TASK-003 startup/WebRTC verification. Do not advance to TASK-004 until TASK-003 has real startup/WebRTC evidence.

## Status vocabulary

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: authorized and actively being executed.
- `PARTIAL`: useful work completed but acceptance criteria not fully met.
- `BLOCKED`: cannot proceed without a concrete dependency.
- `DONE`: acceptance criteria passed with evidence.
- `DEFERRED`: intentionally postponed by product decision.
