# Roadmap

## M0 — Project bootstrap

Repository, environment audit, upstream lock, secret protections and Codex execution discipline.

Current gate: `TASK-000` is done. The locked LiveTalking checkout exists under ignored `third_party/LiveTalking`; see `docs/evidence/TASK-000/environment-audit.md`.

## M1 — Phase 1 Android large-screen voice RAG MVP

Current first priority is Android + Gateway + real ASR/TTS/LLM providers + lightweight RAG. Phase 1 does not run LiveTalking, Wav2Lip, MuseTalk, WebRTC digital-human mode or GPU inference.

Target flow:

`Android recording → Doubao ASR → lightweight RAG retrieval → LLM grounded answer → Doubao TTS → Android playback and subtitles → idle video`

## M2 — Android kiosk and audio foundation

Landscape immersive APK, local idle character video, endpoint configuration, device diagnostics, USB/default microphone recording and speaker playback. Local source/build work is available; final Android hardware acceptance is deferred to M7/TASK-015.

## M3 — Gateway and providers

FastAPI Gateway, request IDs, sanitized logs, ASR/LLM/TTS/Embedding/Knowledge Provider interfaces, Doubao ASR/TTS, Doubao/Volcengine Ark LLM, OpenAI-compatible fallback and cost/error guards.

## M4 — Lightweight RAG

SQLite metadata store, Markdown/TXT/PDF/DOCX parsing, Embedding API, local FAISS Top-K retrieval, approved/draft/rejected content status, source citations, forbidden topics and transfer-to-human behavior. No Dify, LangFlow or Flowise.

## M5 — End-to-end store pilot

Android → ASR → RAG/LLM → TTS → playback/subtitles → idle video, with logs, fallback and privacy controls.

## M6 — Production deployment

Tencent Cloud CPU Gateway, TLS, device auth, monitoring, backup and rollback. No GPU inference on the 8C/4G server.

## M7 — Android device acceptance

U-disk/ADB installation as available, Android 12 real-device validation, USB mic, speaker, network recovery, reboot and long-run checks.

## M8 — Future LiveTalking enhancement

Only after Phase 1 acceptance: re-open deferred LiveTalking/Wav2Lip/MuseTalk/WebRTC work, validate GPU/runtime/FPS, then add `livetalking_webrtc` display mode behind configuration.

See also:

- `docs/architecture/MVP_ARCHITECTURE.md`
- `docs/architecture/FUTURE_LIVETALKING_UPGRADE.md`
- `docs/api/MVP_API_SPEC.md`
- `docs/testing/MVP_ACCEPTANCE.md`
- `docs/testing/REAL_API_ACCEPTANCE.md`
- `docs/operations/MVP_DEPLOYMENT.md`
