# PROJECT_STATE

- **Project:** jiyangjia-android-ai
- **State version:** 0.1.4
- **Updated:** 2026-08-07
- **Overall status:** TASK-015A local avatar dialogue is PARTIAL; TASK-015 remains NO-GO/BLOCKED pending a device and formal release inputs
- **Current authorized task:** finish the manual browser microphone check for TASK-015A; TASK-015 resumes only when its remaining external gates are available
- **Public repository target:** `archibald80000-ai/jiyangjia-android-ai`

## Verified facts

- Main branch (`origin/main`) commit: `a68f234` (TASK-014A administration and display controls included).
- User-approved portrait source media is available at `E:\work\ai-kefu\资料库\人像背景.MOV`; the source was not modified or committed.
- A local ignored H.264 1080x1920 portrait MP4/background pair is published on the isolated `18084` Gateway and bound to the default 9:16 Profile.

- Android target system: Android 12.
- Existing cloud server observed on 2026-08-06: Tencent Cloud IP `120.53.86.89`, Ubuntu `24.04.4 LTS`, 2 CPU cores, about `1.9Gi` memory, 50G disk, 10 Mbps, no GPU.
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
- TASK-009 implemented a Doubao/Volcengine V3 unidirectional TTS adapter behind the TTS Provider interface, plus legacy V1 compatibility, CLI and unit tests.
- TASK-009 Mock TTS CLI generated deterministic bytes with SHA-256 `248253DDDE4121C7512AF5E387BAAEC4EE48C7530D0EAB16F03A31D5DBFC9427`.
- TASK-009 real Doubao TTS V3 call succeeded using private external env file `E:\work\ai-kefu\.env.local`; values were not printed. Output was `audio/mpeg`, `20589` bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`.
- TASK-010 implemented a Doubao/Volcengine WebSocket ASR adapter behind the ASR Provider interface. Real ASR succeeded using private external env file `E:\work\ai-kefu\.env.local`; values were not printed. MP3 input was normalized to 16 kHz mono WAV and recognized as `您好，欢迎来到机养家。`.
- TASK-011 implemented OpenAI-compatible LLM and Embedding adapters behind the Gateway Provider interfaces, with DeepSeek, Doubao/Volcengine Ark and generic OpenAI-compatible configuration slots.
- TASK-011 local backend regression passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\llm tests\gateway tests\asr tests\tts -q` -> 25 passed.
- TASK-011 real DeepSeek LLM smoke call succeeded using private external env file `E:\work\ai-kefu\.env.local`; values were not printed and usage metadata was present.
- TASK-011 real Doubao/Volcengine Ark LLM smoke call succeeded using private external env file `E:\work\ai-kefu\.env.local`; values were not printed and usage metadata was present.
- TASK-011 Doubao/Ark Embedding adapter now supports both plain text `/embeddings` and vision/multimodal `/embeddings/multimodal` routes.
- TASK-011 real Doubao/Ark Embedding smoke call succeeded using the current authorized account and private external env file `E:\work\ai-kefu\.env.local`; values were not printed. The verified default model path is `doubao-embedding-vision-251215`, returning 1 vector with 2048 dimensions and usage metadata present.
- TASK-012 implemented the Phase 1 lightweight RAG layer with SQLite document/chunk metadata, SQLite FTS5 keyword retrieval, FAISS Top-K vector retrieval, explicit Markdown/TXT/PDF/DOCX/JSON/YAML ingestion, approved/draft/rejected status gates, prohibited-topic policy, safe transfer behavior and source citations.
- TASK-012 added a scoped manually reviewed demo FAQ set under `knowledge-test/faq_mvp_approved.example.json` with 10 approved entries, 1 draft entry and 1 rejected entry. It did not scan or import `E:\work\积养家`.
- TASK-012 local knowledge tests passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge -q` -> 6 passed.
- TASK-012 backend regression passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q` -> 34 passed.
- TASK-012 Mock RAG evaluation passed 24/24 cases.
- TASK-012 real Doubao/Ark Embedding RAG evaluation passed 24/24 cases with `doubao-embedding-vision-251215`, vector dimensions 2048, using private external env; secret values were not printed.
- TASK-012 Gateway API smoke passed for real embedding-backed `/api/v1/knowledge/index`, `/api/v1/knowledge/search` and `/api/v1/knowledge/status`.
- TASK-013 implemented Android-to-Gateway dialogue client code: PCM recording is wrapped as WAV, uploaded to `/api/v1/dialogue/audio`, `request_id` is propagated, transcript/answer/source diagnostics are displayed, generated TTS audio is fetched from `/api/v1/audio/{audio_id}`, encoded audio is played through `MediaPlayer`, cancel returns to idle fallback.
- TASK-013 backend E2E tests passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\e2e -q` -> 3 passed.
- TASK-013 backend full regression passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\e2e tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q` -> 37 passed.
- TASK-013 30-cycle Mock Gateway dialogue report passed 30/30 cycles, failed 0, fallback count 0; local TestClient average latency 4.33 ms.
- TASK-013 real private-env Gateway smoke passed with Doubao ASR, Doubao/Ark Embedding, Doubao/Ark LLM and Doubao TTS; generated answer audio fetch returned HTTP 200, `audio/mpeg`, `69741` bytes, latency `13623` ms. Secret values were not printed.
- TASK-013 Android local unit tests, `assembleDebug` and `lintDebug` passed using project-local Temurin JDK 17 and Android SDK.
- TASK-013 generated debug APK `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `862144` bytes, SHA-256 `263B1FA8E8DB2198E93B4E4FFC85E715CEE2556E0511C67B002D7E588C76BC8E`, package `ai.jiyangjia.kiosk.debug`, version `0.1.0-task013-debug`.
- TASK-013 follow-up hardening added Gateway transcript normalization for the brand name `积养家`. Common ASR homophones such as `机养家`, `季养家`, `寄养家`, `吉阳家`, `积阳家` and `济氧家` are normalized before RAG/LLM; original provider output is preserved as `transcript.raw_text` when changed.
- TASK-013 brand normalization regression passed: `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\asr tests\gateway tests\e2e -q` -> 19 passed, and full backend regression -> 42 passed.
- TASK-014 server-thread evidence was imported on 2026-08-06 and re-verified after full remediation.
- `/opt/jiyangjia-ai/secrets/.env.local` exists and is mounted via compose with secure mode and no root `.env` override.
- `scripts/check_provider_env.py --require-real-mvp` now reports `asr/tts/llm/embedding` provider readiness as `true`.
- TASK-014 now exposes `/api/v1/readiness` and the production `/api/v1/*` MVP chain returns real, non-blocking results:
  - `/health`
  - `/api/v1/health`
  - `/api/v1/readiness`
  - `/api/v1/client/config`
  - `/api/v1/knowledge/status`
  - `/api/v1/knowledge/index`
  - `/api/v1/knowledge/search`
  - `/api/v1/dialogue/text` (real ASR + RAG + LLM + TTS)
  - `/api/v1/dialogue/audio` (real ASR + RAG + LLM + TTS)
  - `/api/v1/audio/{audio_id}` (audio fetch 200, `audio/mpeg`, bytes returned)
- `tasks/TASK-014_TENCENT_GATEWAY_DEPLOYMENT.md` close-out evidence now includes request IDs, sources, audio IDs and latency/failure details.

## Not yet verified

- Android CPU architecture and screen resolution.
- USB Host / USB Audio Class support.
- Whether APK sideloading and ADB are enabled.
- Phase 1 Android install and idle video/local fallback behavior on an Android device.
- USB/default microphone recording on target Android 12 display.
- Speaker playback and subtitle behavior on target Android 12 display.
- USB microphone physical unplug/replug recovery on target hardware.
- Formal production knowledge base beyond the 10 approved demo FAQ entries.
- Android 12 real-device install, recording, Gateway upload, TTS playback and subtitle visual validation.
- Tencent Cloud full MVP Gateway deployment is now closed: 2026-08-07 验证了 real provider chain 与 9 项关键接口（含 Dialogue text/audio），不再以 Provider 503 阻塞。
- LiveTalking model weights, WebRTC connectivity and Wav2Lip/MuseTalk runtime behavior are deferred to the future enhancement phase.
- OpenAI-compatible fallback LLM with a third provider beyond DeepSeek/Doubao.
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
- `docs/evidence/TASK-009/tts-provider.md`
- `docs/evidence/TASK-009/task009-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-tts-cli-missing-credentials-20260806.txt`
- `docs/evidence/TASK-009/task009-v3-pytest-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-config-preflight-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-real-call-20260806.txt`
- `docs/evidence/TASK-009/task009-doubao-v3-ffprobe-20260806.txt`
- `docs/evidence/TASK-010/asr-provider.md`
- `docs/evidence/TASK-010/task010-doubao-asr-config-preflight-20260806.txt`
- `docs/evidence/TASK-010/task010-doubao-asr-real-call-mp3-normalized-20260806.txt`
- `docs/evidence/TASK-010/task010-pytest-final-20260806.txt`
- `docs/evidence/TASK-011/llm-provider.md`
- `docs/evidence/TASK-011/task011-pytest-final-20260806.txt`
- `docs/evidence/TASK-011/task011-deepseek-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-real-call-rejected-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-real-call-authorized-20260806.txt`
- `docs/evidence/TASK-011/task011-pytest-after-embedding-authorized-20260806.txt`
- `docs/evidence/TASK-012/lightweight-rag.md`
- `docs/evidence/TASK-012/task012-pytest-knowledge-20260806.txt`
- `docs/evidence/TASK-012/task012-pytest-full-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-mock-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-doubao-embedding-20260806.txt`
- `docs/evidence/TASK-012/task012-gateway-real-embedding-api-smoke-20260806.txt`
- `docs/evidence/TASK-013/end-to-end-dialogue.md`
- `docs/evidence/TASK-013/task013-30cycle-pytest-report.json`
- `docs/evidence/TASK-013/task013-pytest-e2e-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-20260806.txt`
- `docs/evidence/TASK-013/task013-android-unit-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-assemble-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-lint-final-20260806.txt`
- `docs/evidence/TASK-013/task013-apk-verification-20260806.txt`
- `docs/evidence/TASK-013/task013-brand-normalization-samples-20260806.txt`
- `docs/evidence/TASK-013/task013-brand-normalization-pytest-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-after-brand-normalization-20260806.txt`
- `docs/evidence/TASK-014/server-evidence-reconciliation-20260806.md`
- `docs/evidence/TASK-014/server-redeployment-request-20260806.md`
- `docs/evidence/TASK-014/task014-provider-env-check-after-recreate-20260807.json`
- `docs/evidence/TASK-014/task014-acceptance-summary-20260807-0943.json`
- `docs/evidence/TASK-014/task014-dialogue-audio-retry-20260807-0944.json`
- `docs/evidence/TASK-014/task014-final-acceptance-20260807.json`
- `docs/evidence/TASK-014/task014-gateway-build-final-20260807.txt`
- `docs/evidence/TASK-014/task014-provider-env-final-20260807.json`
- `docs/evidence/TASK-014/task014-knowledge-cleanup-final-20260807.json`
- `docs/evidence/TASK-014/task014-redeployment-local-pytest-20260806.txt`
- `docs/evidence/TASK-014/task014-docker-compose-parse-20260806.txt`
- `docs/evidence/TASK-014/task014-redeployment-verify-repository-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-pytest-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-compose-parse-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-missing-sample-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-ready-sample-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-verify-repository-20260806.txt`
- `docs/evidence/TASK-014/task014-provider-env-preflight-secret-scan-20260806.txt`

Recent task results:

- DONE. `scripts/bootstrap_livetalking.ps1` completed with process-scoped Git config `http.version=HTTP/1.1`; `third_party/LiveTalking` is a real ignored Git checkout at `c963ad409c556918b7d23999bf87c47a7c05c932`. No model weights or avatar packages were downloaded.
- TASK-001 DONE. Upstream README/API/config/source/license were audited and summarized. Static endpoint and integration boundaries are recorded in `docs/evidence/TASK-001/upstream-audit.md` and `docs/03_LIVETALKING_SCOPE.md`. No service, model, WebRTC or provider runtime success is claimed.
- TASK-002 DONE. A local ignored Conda runtime was created at `.venv\livetalking-task002`; PyTorch CUDA and LiveTalking dependency import checks passed. No model, avatar, service startup, WebRTC or provider success is claimed.
- TASK-003 DEFERRED. Required Wav2Lip model/S3FD/avatar assets are still absent, but this no longer blocks Phase 1 because LiveTalking/WebRTC/GPU inference moved to the future enhancement phase. No LiveTalking startup/WebRTC/FPS success is claimed.
- ROUTE UPDATED. Phase 1 design documents now define the Android idle-video voice FAQ MVP and keep future LiveTalking integration behind extension interfaces.
- TASK-005 DONE. Android kiosk shell source implementation is present and local Gradle build/unit tests/lint/APK generation passed. Android 12 real-device install/rendering is not claimed because `adb devices` returned no connected device.
- TASK-007 PARTIAL. Android audio diagnostics, USB-first routing policy, runtime permission, bounded in-memory recording, local playback and audio device add/remove monitoring are implemented and locally verified by Gradle/lint/APK build. Real USB microphone, speaker and physical unplug/replug behavior are not verified because no Android device was connected.
- TASK-008 DONE. Local FastAPI Gateway skeleton, ASR/TTS/LLM/Embedding Provider interfaces, Mock orchestration, SQLite knowledge skeleton, request IDs and required API endpoints are implemented and verified by pytest plus local HTTP checks on port 18080. No real provider/API success or production deployment is claimed.
- TASK-009 DONE. Doubao TTS adapter now uses the official V3 unidirectional HTTP streaming protocol by default, retains V1 compatibility, and is verified by 10 local tests plus one real private-env API call. Generated MP3 evidence: `audio/mpeg`, 24 kHz mono, 2.568 seconds, `20589` bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`. Android playback of that audio is still deferred to TASK-013/TASK-015.
- TASK-010 DONE. Doubao ASR adapter uses the official big-model WebSocket protocol through a bounded Gateway file/bytes-to-chunks path. `python -m pytest tests\asr tests\gateway tests\tts -q` passed with 16 tests. Real ASR with private env succeeded for generated TTS smoke audio after MP3-to-WAV normalization; observed transcript was `您好，欢迎来到机养家。`, with one domain-name character error to handle in later vocabulary/RAG policy.
- TASK-011 DONE. OpenAI-compatible LLM and Embedding adapters are implemented with tests and CLI smoke tools. Real DeepSeek and Doubao/Volcengine Ark LLM calls succeeded using private env. Real Doubao/Ark Embedding now succeeds with `doubao-embedding-vision-251215`, returning 2048-dimensional vectors.
- TASK-012 DONE. Lightweight RAG now indexes explicitly selected approved/draft/rejected documents into SQLite metadata, FTS5 and FAISS; returns Top-K sources; blocks prohibited topics; and passed Mock plus real Doubao/Ark Embedding evaluation. No raw `E:\work\积养家` import, Android E2E, Tencent deployment or real-device success is claimed.
- TASK-013 PARTIAL. Android client code now implements the record -> Gateway audio dialogue -> fetch TTS -> playback/subtitles -> idle fallback loop and builds successfully. Backend Mock 30-cycle and one real provider Gateway smoke passed. Android 12 real-device recording/playback/subtitle behavior is not claimed because no device was attached.
- TASK-013 FOLLOW-UP. Gateway now normalizes common ASR homophones of `积养家` before retrieval and answer generation while preserving `raw_text` for audit/debugging.
- TASK-014 DONE. The Gateway-only image was rebuilt and force-recreated on Tencent Cloud. The online container is healthy and includes FFmpeg `7.1.5-0+deb13u1`; `/api/v1/readiness` reports all real providers ready.
- TASK-014 final acceptance passed once for text, Android-format 16 kHz mono PCM WAV, MP3 compatibility, ASR, approved-only RAG, LLM, TTS, sources, request IDs, audio IDs and downloadable `audio/mpeg`.
- TASK-014 knowledge cleanup downgraded eight conflicting deployment test records to `draft`. Customer-facing `approved` knowledge now contains only the 10 controlled TASK-012 FAQ entries. Rollback backup: `/opt/jiyangjia-ai/backups/task014-knowledge-cleanup-20260807-125648`.
- TASK-014A is DONE locally after correcting a browser action-dispatch defect. Knowledge upload/preview/approve/publish/reject/search/dialogue, asset upload/preview/publish/rollback/delete, Display Profile create/edit/bind/default and system refresh were clicked in a real browser and changed backend state. Full pytest passed 55 tests; no application console errors were observed. TASK-014A is not deployed to Tencent Cloud and has no formal business media or Android device evidence.
- TASK-014C is PARTIAL. Gateway bootstrap/config/manifest/profile responses now use versioned strong ETags, and Android performs validated staging, SHA-256 verification, active/previous pointer switching, offline startup, foreground polling and bounded background recovery. Local Gateway and Android tests pass; trusted production HTTPS, approved media and device acceptance are unavailable.
- TASK-014D is PARTIAL. Media3 now applies background/character/subtitle/control layers and Display Profile geometry, switches video on first frame, and invokes TASK-014C rollback on decoder failure. Four viewport geometry tests and Android test/lint/debug assembly pass; screenshot baselines and a physical display remain unavailable.
- TASK-014E is PARTIAL. Gateway and Android implement 16 kHz mono PCM16 streaming, exact 20 ms frames, WebRTC VAD, partial/final events, single WAV fallback, generation cancellation and AEC-aware automatic barge-in. Full Gateway regression passed 61 tests and Android test/lint/debug assembly passed. A controlled real Doubao `bigmodel_async` call produced three partials and one final; Android 12 USB/AEC latency and false-trigger acceptance remain unavailable.
- TASK-014F is PARTIAL. The APK contains a minimal DPC, DeviceAdminReceiver, persistent Home configuration, BootReceiver and guarded Lock Task entry. Runtime diagnostics distinguish `managed_locked` from `limited_unmanaged`. Android unit/build/lint pass, but this workstation has no emulator package/system image and `adb devices -l` is empty, so Device Owner/reboot behavior is not claimed.
- TASK-014G is PARTIAL. Release builds require externally supplied monotonic version/signing parameters; Gateway release metadata fails closed; Android verifies HTTPS, size, file hash, package, newer version and signing identity before PackageInstaller. Mock policy/release-manifest tests pass. A disposable test-only certificate produced a v1/v2/v3-verified package and was deleted; no formal key, trusted release URL or device upgrade acceptance exists.
- TASK-015 is BLOCKED with a NO-GO decision. Gateway regression passed 63 tests, Android unit/lint/debug assembly and repository verification pass, but `adb devices -l` is empty and the local SDK has no emulator/system image. USB/AEC, visual, reboot, true Lock Task, formal update/rollback and long-run gates are untested.
- TASK-015A is PARTIAL. The rights-confirmed portrait source was converted to an ignored H.264 1080x1920 silent MP4 plus JPG background, published and bound to the 9:16 Profile. A real local browser dialogue passed RAG, Doubao LLM/TTS, sources, request ID, audio fetch and visible subtitle playback. Browser recording now supports manual end/send plus speech-first 3-second silence auto-send; browser microphone permission and Android device behavior remain manual/unverified.

Next action:

- At `http://127.0.0.1:18084/demo/kiosk`, manually grant microphone permission and run one spoken question. Then resume TASK-015 only after Android device/audio hardware, trusted HTTPS hosting and formal signing identity with N/N+1/N+2 candidates are available. Production rollout is still not authorized.

## Status vocabulary

- `PLANNED`: documented but not started.
- `IN_PROGRESS`: authorized and actively being executed.
- `PARTIAL`: useful work completed but acceptance criteria not fully met.
- `BLOCKED`: cannot proceed without a concrete dependency.
- `DONE`: acceptance criteria passed with evidence.
- `DEFERRED`: intentionally postponed by product decision.
