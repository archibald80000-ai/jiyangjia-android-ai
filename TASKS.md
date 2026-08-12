# Task index

The canonical machine-readable index is [`tasks/index.yaml`](tasks/index.yaml). Human-readable instructions are in [`tasks/README.md`](tasks/README.md).

Current status:

- `TASK-000`: `DONE`; environment/repository audit passed and LiveTalking locked checkout exists under ignored `third_party/LiveTalking`.
- `TASK-001`: `DONE`; locked LiveTalking upstream source audited with endpoint, model/asset, network, extension and compliance notes.
- `TASK-002`: `DONE`; isolated LiveTalking runtime exists under ignored `.venv\livetalking-task002`, dependencies/imports/PyTorch CUDA smoke check passed.
- `TASK-003`: `DEFERRED`; Wav2Lip/LiveTalking asset-dependent baseline is moved to a future enhancement phase and no longer blocks Phase 1.
- `TASK-004`: `DEFERRED`; LiveTalking API automation waits until the future enhancement phase.
- `TASK-005`: `DONE`; Android Kotlin landscape kiosk shell, local idle-video path handling, offline fallback visual, non-secret config entry, Gradle Wrapper, unit tests, lint and debug APK build passed. APK SHA-256: `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`.
- `TASK-006`: `DEFERRED`; LiveTalking display mode is deferred; local idle video is folded into TASK-005 for Phase 1.
- `TASK-007`: `PARTIAL`; Android runtime microphone permission, device diagnostics, USB-first input preference, bounded in-memory recording, local playback and source-side audio device change monitoring are implemented and locally built/tested, but real Android 12 USB microphone/speaker/physical unplug recovery validation is blocked by no connected device. APK SHA-256: `B2FEBA1C2E2A69D0AE2ED43DB000D75F0EA1BC67D396E9ECE22F8512A4D22D49`.
- `TASK-008`: `DONE`; local FastAPI Gateway and unified Provider skeleton are implemented and tested. Required API endpoints, Mock ASR/TTS/LLM/Embedding providers, SQLite knowledge skeleton, request IDs and audio fetch are verified. No real provider/API or production deployment success is claimed.
- `TASK-009`: `DONE`; Doubao/Volcengine TTS adapter now defaults to official V3 unidirectional HTTP streaming, retains legacy V1 compatibility, passes local tests, and generated a real private-env MP3 (`audio/mpeg`, 20589 bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`). No Android playback success is claimed yet.
- `TASK-010`: `DONE`; Doubao/Volcengine ASR adapter uses the official big-model WebSocket protocol through a bounded Gateway file/bytes-to-chunks path, passes local tests, and recognized generated TTS smoke audio after MP3-to-WAV normalization. Observed transcript: `您好，欢迎来到机养家。`.
- `TASK-011`: `DONE`; OpenAI-compatible LLM and Embedding adapters are implemented and locally tested. Real DeepSeek and Doubao/Volcengine Ark LLM calls succeeded with private env. Real Doubao/Ark Embedding now succeeds with the authorized account using `doubao-embedding-vision-251215`, returning 2048-dimensional vectors.
- `TASK-012`: `DONE`; lightweight RAG is implemented with SQLite metadata, SQLite FTS5, FAISS Top-K retrieval, approved/draft/rejected status gates, prohibited-topic safe transfer, explicit document parsing and source citations. Mock evaluation passed 24/24 cases; real Doubao/Ark Embedding evaluation passed 24/24 cases with 2048-dimensional vectors. No raw `E:\work\积养家` import is claimed.
- `TASK-013`: `PARTIAL`; Android now records PCM, uploads WAV to Gateway, carries request IDs, displays transcript/answer/source diagnostics, downloads generated TTS audio and plays encoded answer audio before returning to idle fallback. Backend E2E passed 30/30 Mock cycles and one real private-env Doubao ASR -> RAG -> Doubao/Ark LLM -> Doubao TTS smoke. Gateway now normalizes common ASR homophones of `积养家` while preserving `raw_text`. Android 12 real-device install/record/playback/subtitle validation is not claimed because `adb devices -l` returned no attached devices.
- `TASK-014`: `DONE`; Tencent Cloud Gateway-only image was rebuilt and force-recreated with online FFmpeg `7.1.5-0+deb13u1`. Real Provider readiness passed. One final acceptance passed for text, Android-format WAV, MP3, ASR, approved-only RAG, LLM, TTS, sources, request IDs, audio IDs and audio downloads. Eight conflicting deployment test records were downgraded to `draft`; approved knowledge is the 10 controlled TASK-012 FAQ entries. Evidence:
  - `docs/evidence/TASK-014/task014-final-acceptance-20260807.json`
  - `docs/evidence/TASK-014/task014-gateway-build-final-20260807.txt`
  - `docs/evidence/TASK-014/task014-provider-env-final-20260807.json`
  - `docs/evidence/TASK-014/task014-knowledge-cleanup-final-20260807.json`.
- `TASK-014A`: `DONE` in `main` after browser interaction repair; 55 tests plus real-browser action verification passed:
  - 系统状态页
  - 知识库审批与索引页
  - 数字人素材管理页
  - 多分辨率 Display Profile 配置页
  - evidence: `docs/evidence/TASK-014A/`
  - real-browser evidence: `task014a-real-browser-actions-20260807.json`
  - not yet deployed to Tencent Cloud; no formal media/business content or Android device result is claimed.
- `TASK-015A`: `PARTIAL`; the user-approved portrait MOV was prepared as an ignored H.264 1080x1920 MP4 plus JPG background, published locally, bound to the default 9:16 Profile, and verified through a real browser RAG/LLM/TTS dialogue. Recording supports manual end/send and speech-first 3-second silence auto-send. Browser microphone permission remains a manual check; no Android device result is claimed. Evidence: `docs/evidence/TASK-015A/local-avatar-dialogue-demo-20260807.md`.
- `TASK-014H`: `DONE`; canonical DNS/HTTPS/Nginx/Gateway and Android production Base URL are active. HTTP redirects 308 to HTTPS, root and Demo return HTML 200, public APIs work, and Certbot renewal dry-run passed on 2026-08-12.
- `TASK-015`: `PARTIAL / ANDROID_13_SMOKE_PASS`; startup crash recovery, built-in microphone capture, three-second silence send, real ASR/RAG/LLM/TTS, speaker playback and return to idle passed on a Xiaomi Android 13 phone. Android 12 store-screen USB microphone, external speaker, reboot, managed Lock Task, formal signing/update rollback and long-run acceptance remain open. Evidence: `docs/evidence/TASK-015/android13-launch-audio-smoke-20260812.md`.
- `TASK-015B`: `PARTIAL / PUBLIC_STREAM_AND_PHONE_NAV_PASS`; malformed browser generations now fail as `INVALID_START`, production WSS passed real Doubao ASR/RAG/LLM/TTS with sources and audio fetch, and v9 / `0.1.8` phone/store APKs are published separately. The phone package passed three cold launches and normal Home/recents/notification navigation. MIUI rejected instrumentation installation with `INSTALL_FAILED_USER_RESTRICTED`, and human browser-microphone speech remains a manual gate. Evidence: `docs/evidence/TASK-015B/task015b-public-voice-phone-mode-20260812.md`.
- `TASK-020A`: `DONE`; the reviewed v2.1 package was imported through an isolated port-8090 Gateway using real Doubao Embedding. Final state is 41 approved, 24 draft, 65 chunks and 65 FAISS vectors at 2048 dimensions. Current-policy evaluation passed 80/80, sources were complete for 80/80 responses and draft leaks were 0. The old exact-label score remains 42/80 because the unchanged test file predates draft-shadow and scoped safety routing. The active demo database was backed up and preserved. Evidence: `docs/evidence/TASK-020A/formal-knowledge-import-acceptance-20260807.md`.
- `TASK-020B`: `DONE` locally; the accepted candidate was bound to the isolated port-18084 9:16 avatar demo with real Doubao ASR/TTS/LLM/Embedding. A real WAV normalized `七养家` to `积养家`, matched approved sources and returned downloadable MP3 TTS. Browser text dialogue, 1080x1920 playback and return-to-idle passed. Local source paths are redacted from public citations. Evidence: `docs/evidence/TASK-020B/avatar-knowledge-binding-20260807.md`.
- `TASK-020C`: `PARTIAL / BLOCKED_BY_TENCENT_WEBBLOCK_ICP`; Tencent production now has the 41 approved/24 draft formal knowledge state, the approved MOV-derived 1080x1920 video/background and a bound default Profile. Real production RAG/LLM/TTS and source redaction passed. Server-local canonical HTTPS is 200; external HTTPS is still reset, so public sharing is not DONE. Evidence: `docs/evidence/TASK-020C/production-knowledge-avatar-sharing-20260807.md`.
- `TASK-020D`: `DONE`; the user-authorized v2.1 knowledge is available as public GitHub JSON under `knowledge-public/v2.1/`. Production was backed up and re-indexed in 50+15 batches with real Doubao Embedding; final state is 41 approved, 24 draft, 65 vectors at 2048 dimensions. Current-policy production search passed 80/80 with zero draft leaks and complete sources. Evidence: `docs/evidence/TASK-020D/public-knowledge-package-import-20260807.md`.
- `TASK-020E`: `DONE / READY_FOR_DEMO`; a new port-8091 candidate imported the two v2.1 batches with real Doubao Embedding and retained 41/24 documents plus 65 x 2048 FAISS vectors. Search passed 80/80 with approved Top-3 36/36, sources 100% and zero draft leaks. Five synthetic-speech audio requests passed real ASR/RAG/LLM/TTS and audio fetch after scoped short-query and `七膳` ASR normalization. Existing demo and old indexes were backed up and preserved. Evidence: `docs/evidence/TASK-020E/gateway-real-import-acceptance-20260808.md`.
- `TASK-020F`: `DONE / PRODUCTION_PUBLISHED`; 25 authorized Aiye HTML files are publicly archived with SHA-256. v2.2 preserves 65 v2.1 records and adds 139 approved `aiye_` records for a 204-document production state. Real Doubao Embedding produced 340 x 2048 vectors; local and production Top-3 search passed 240/240 with sources 100% and draft leaks 0. Six text and one synthetic-speech audio flow passed the real production chain. Rollback: `/opt/jiyangjia-ai/backups/task020f-20260809T035803Z`. Evidence: `docs/evidence/TASK-020F/aiye-knowledge-v22-acceptance-20260809.md`.
- `TASK-020G`: `DONE / PRODUCTION_PUBLISHED`; the authorized 135-file public training site is archived under `knowledge-public/v2.3/site/`. v2.3 preserves all 204 v2.2 records and adds 47 data-generated approved products. Production is 227 approved, 24 draft and 387 x 2048 real Doubao vectors. Product Top-3 passed 141/141, sources 100%, draft leaks 0, and real public RAG/LLM/TTS plus audio fetch passed. Rollback: `/opt/jiyangjia-ai/backups/task-v23-production-20260812-024528`. Evidence: `docs/evidence/TASK-020G/public-site-knowledge-v23-acceptance-20260812.md`.
- `TASK-020H`: `DONE / PRODUCTION_PUBLISHED`; deterministic LF output repaired the v2.3 manifest hashes. The later-authorized six-soup and seven-soup HTML files are archived under `knowledge-public/v2.4/sources/` and add 15 draft records without changing the 227 approved records. Production is 227 approved, 39 draft and 402 x 2048 real Doubao vectors. Approved-product Top-3 passed 141/141, 43 new draft questions leaked 0 records, and real public RAG/LLM/TTS plus audio fetch passed. Rollback: `/opt/jiyangjia-ai/backups/task020h-20260812T150643Z`. Evidence: `docs/evidence/TASK-020H/knowledge-v24-integrity-production-sync-20260812.md`.

Current order:

Phase 1 execution order from the current route:

`TASK-008 → TASK-009 → TASK-010 → TASK-011 → TASK-012 → TASK-013 → TASK-014 → TASK-014A → TASK-015`

Local presentation side task: `TASK-015A(PARTIAL)`; it removes the missing-media blocker locally but does not replace TASK-015 device acceptance.

Public voice/mobile side task: `TASK-015B(PARTIAL)`; public streaming and phone-safe navigation pass, but the bounded MIUI install/instrumentation and human-microphone checks remain.

Production domain gate: `TASK-014H(DONE)`; public HTTPS and renewal validation now pass.

Knowledge demo gate: `TASK-020A(DONE) -> TASK-020B(DONE locally) -> TASK-020C(PARTIAL historical) -> TASK-020D(DONE) -> TASK-020E(DONE) -> TASK-020F(DONE) -> TASK-020G(DONE) -> TASK-020H(DONE / v2.4 production published)`.

Completed foundation retained from earlier tasks:

`TASK-000 → TASK-005 → TASK-007(PARTIAL source/local only)`

Future enhancement:

`TASK-003/TASK-004/TASK-006/TASK-016` for LiveTalking / Wav2Lip / MuseTalk / WebRTC digital human work.

Do not execute multiple implementation tasks concurrently unless a later task explicitly permits parallel work.

- 2026-08-07：TASK-014 最终收口通过。线上容器包含 FFmpeg；Android WAV 与 MP3 都通过真实 ASR/RAG/LLM/TTS 和音频下载链路。
 - 下一步：取得 Android 12 真机和已批准素材/Profile 后，仅执行 `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md`；TASK-014A 生产部署另行授权。

**当前仓库基线更新：`main` 已包含 `TASK-014A`，当前任务序列已对齐到 `TASK-015`。**
