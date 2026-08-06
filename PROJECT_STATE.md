# PROJECT_STATE

- **Project:** jiyangjia-android-ai
- **State version:** 0.1.0
- **Updated:** 2026-08-06
- **Overall status:** TASK-008 DONE - FASTAPI GATEWAY AND PROVIDER SKELETON VERIFIED LOCALLY
- **Current authorized task:** TASK-009 (real Doubao TTS adapter)
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
- TASK-003 checked `E:\work\ai-kefu\livetalking-assets` on 2026-08-06; the directory does not exist, so no real official Wav2Lip assets are available for installation.
- Product route changed on 2026-08-06: Phase 1 defers LiveTalking/Wav2Lip/MuseTalk/WebRTC digital-human and GPU inference. The current MVP is Android idle character video + tap-to-talk + FastAPI Gateway + real Doubao ASR/TTS + Doubao/Volcengine Ark or OpenAI-compatible LLM + Embedding API + SQLite/FAISS lightweight RAG + subtitles.
- Android real-device validation is deferred to TASK-015 and does not block local Gateway/provider/RAG development.
- ADR-0008 records the Phase 1 idle-video voice FAQ MVP decision.
- TASK-005 created an Android Kotlin app scaffold under `android-app/` with package `ai.jiyangjia.kiosk`, version `0.1.0-task005`, landscape immersive `KioskActivity`, local idle-video path handling, offline animated fallback visual, non-secret development config and first-pass client state/unit-test source files.
- TASK-005 generated and committed the official Gradle Wrapper for Gradle `8.10.2`.
- TASK-005 installed a local ignored Android toolchain cache under `.cache/android-toolchain`: Temurin JDK `17.0.20+8`, Android command-line tools, platform-tools `37.0.1-15733141`, `platforms;android-35` and build tools.
- TASK-005 Gradle `tasks`, `testDebugUnitTest assembleDebug` and `lintDebug` completed successfully.
- TASK-005 generated debug APK `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `830932` bytes, SHA-256 `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`.
- TASK-005 `aapt dump badging` confirmed package `ai.jiyangjia.kiosk.debug`, minSdk `23`, targetSdk `35`, and launch activity `ai.jiyangjia.kiosk.KioskActivity`.
- TASK-005 repository verification and whitespace checks passed.
- TASK-007 implemented Android runtime microphone permission, audio device diagnostics, USB-first input preference, fallback to system input, bounded in-memory PCM recording, local playback, audio device add/remove monitoring and lifecycle cleanup.
- TASK-007 local Gradle `testDebugUnitTest assembleDebug` passed with 8 unit tests and no failures.
- TASK-007 `lintDebug` passed after addressing permission and device-enumeration lint issues.
- TASK-007 generated debug APK `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `849801` bytes, SHA-256 `B2FEBA1C2E2A69D0AE2ED43DB000D75F0EA1BC67D396E9ECE22F8512A4D22D49`.
- TASK-007 `aapt dump badging` confirmed `android.permission.RECORD_AUDIO` and the microphone feature are present in the APK.
- TASK-007 `adb devices -l` returned no connected device; `adb shell dumpsys audio` and `adb shell dumpsys usb` failed with `no devices/emulators found`.

## Not yet verified

- Android CPU architecture and screen resolution.
- USB Host / USB Audio Class support.
- Whether APK sideloading and ADB are enabled.
- Phase 1 Android install and idle video/local fallback behavior on an Android device.
- USB/default microphone recording on target Android 12 display.
- Speaker playback and subtitle behavior on target Android 12 display.
- USB microphone physical unplug/replug recovery on target hardware.
- Real provider adapters, FAISS RAG implementation and end-to-end voice RAG loop.
- LiveTalking model weights, WebRTC connectivity and Wav2Lip/MuseTalk runtime behavior are deferred to the future enhancement phase.
- Real Doubao ASR/TTS, Doubao/Volcengine Ark LLM, OpenAI-compatible fallback LLM and Embedding API behavior.
- Production domain, TLS certificate, firewall and TURN strategy.
- Whether the expanded local framework should replace the current GitHub `main` content or be published through a review branch.

## Current milestone

**M1 — Phase 1 Android large-screen voice RAG MVP**

Exit criteria:

- Android 12 app launches in landscape immersive mode and loops local idle character video.
- User can tap to record through USB/default microphone and hear TTS answer through speaker.
- Gateway performs ASR -> lightweight RAG retrieval -> LLM answer -> TTS with request IDs, sources and sanitized logs.
- Knowledge uses selected approved Markdown/TXT/PDF/DOCX documents, SQLite metadata and local FAISS index; no Dify, LangFlow, Flowise or bulk raw-material scan.
- End-to-end store-flow evidence exists with subtitles, audio playback, fallback and rollback notes.

Current evidence:

- `docs/evidence/2026-08-06-local-sync-audit.md`
- `docs/evidence/TASK-000/environment-audit.md`
- `docs/evidence/TASK-001/upstream-audit.md`
- `docs/evidence/TASK-002/environment-matrix.md`
- `docs/evidence/TASK-003/wav2lip-baseline.md`
- `docs/architecture/MVP_ARCHITECTURE.md`
- `docs/api/MVP_API_SPEC.md`
- `docs/testing/MVP_ACCEPTANCE.md`
- `docs/testing/REAL_API_ACCEPTANCE.md`
- `docs/operations/MVP_DEPLOYMENT.md`
- `docs/architecture/LIGHTWEIGHT_RAG.md`
- `docs/evidence/phase1-route-adjustment-20260806.md`
- `docs/evidence/phase1-route-adjustment-final-verification-20260806.txt`
- `docs/evidence/TASK-005/android-shell.md`
- `docs/evidence/TASK-005/task005-verification-20260806.txt`
- `docs/evidence/TASK-005/task005-environment-20260806.txt`
- `docs/evidence/TASK-005/task005-toolchain-install-20260806.txt`
- `docs/evidence/TASK-005/task005-gradle-build-20260806.txt`
- `docs/evidence/TASK-005/task005-lint-20260806.txt`
- `docs/evidence/TASK-005/task005-final-apk-verification-20260806.txt`
- `docs/evidence/TASK-007/android-audio.md`
- `docs/evidence/TASK-007/task007-final-verification-20260806.txt`
- `docs/evidence/TASK-007/task007-device-callback-verification-20260806.txt`
- `docs/evidence/TASK-008/gateway-skeleton.md`
- `docs/evidence/TASK-008/task008-pytest-20260806.txt`
- `docs/evidence/TASK-008/task008-local-server-18080-20260806.txt`

Recent task results:

- DONE. `scripts/bootstrap_livetalking.ps1` completed with process-scoped Git config `http.version=HTTP/1.1`; `third_party/LiveTalking` is a real ignored Git checkout at `c963ad409c556918b7d23999bf87c47a7c05c932`. No model weights or avatar packages were downloaded.
- TASK-001 DONE. Upstream README/API/config/source/license were audited and summarized. Static endpoint and integration boundaries are recorded in `docs/evidence/TASK-001/upstream-audit.md` and `docs/03_LIVETALKING_SCOPE.md`. No service, model, WebRTC or provider runtime success is claimed.
- TASK-002 DONE. A local ignored Conda runtime was created at `.venv\livetalking-task002`; PyTorch CUDA and LiveTalking dependency import checks passed. No model, avatar, service startup, WebRTC or provider success is claimed.
- TASK-003 DEFERRED. Required Wav2Lip model/S3FD/avatar assets are still absent, but this no longer blocks Phase 1 because LiveTalking/WebRTC/GPU inference moved to the future enhancement phase. No LiveTalking startup/WebRTC/FPS success is claimed.
- ROUTE UPDATED. Phase 1 design documents now define the Android idle-video voice FAQ MVP and keep future LiveTalking integration behind extension interfaces.
- TASK-005 DONE. Android kiosk shell source implementation is present and local Gradle build/unit tests/lint/APK generation passed. Android 12 real-device install/rendering is not claimed because `adb devices` returned no connected device.
- TASK-007 PARTIAL. Android audio diagnostics, USB-first routing policy, runtime permission, bounded in-memory recording, local playback and audio device add/remove monitoring are implemented and locally verified by Gradle/lint/APK build. Real USB microphone, speaker and physical unplug/replug behavior are not verified because no Android device was connected.
- TASK-008 DONE. Local FastAPI Gateway skeleton, ASR/TTS/LLM/Embedding Provider interfaces, Mock orchestration, SQLite knowledge skeleton, request IDs and required API endpoints are implemented and verified by pytest plus local HTTP checks on port 18080. No real provider/API success or production deployment is claimed.

Next action:

- Continue exactly one next task: TASK-009 real Doubao TTS adapter. Before coding, verify current official Doubao/Volcengine TTS API docs and required environment variables; if credentials are missing, mark `BLOCKED_PROVIDER_CREDENTIALS` rather than claiming real success.

## Status vocabulary

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: authorized and actively being executed.
- `PARTIAL`: useful work completed but acceptance criteria not fully met.
- `BLOCKED`: cannot proceed without a concrete dependency.
- `DONE`: acceptance criteria passed with evidence.
- `DEFERRED`: intentionally postponed by product decision.
