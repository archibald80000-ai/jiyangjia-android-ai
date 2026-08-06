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
- Next action is to reconcile TASK-014 Tencent Cloud Gateway deployment evidence from the other thread, then continue to TASK-015 Android real-device acceptance.

Current order:

Phase 1 execution order from the current route:

`TASK-008 → TASK-009 → TASK-010 → TASK-011 → TASK-012 → TASK-013 → TASK-014 → TASK-015`

Completed foundation retained from earlier tasks:

`TASK-000 → TASK-005 → TASK-007(PARTIAL source/local only)`

Future enhancement:

`TASK-003/TASK-004/TASK-006/TASK-016` for LiveTalking / Wav2Lip / MuseTalk / WebRTC digital human work.

Do not execute multiple implementation tasks concurrently unless a later task explicitly permits parallel work.
