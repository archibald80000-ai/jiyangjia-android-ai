# Roadmap

## M0 — Project bootstrap

Repository, environment audit, upstream lock, secret protections and Codex execution discipline.

Current gate: `TASK-000` is done. The locked LiveTalking checkout exists under ignored `third_party/LiveTalking`; see `docs/evidence/TASK-000/environment-audit.md`.

## M1 — Phase 1 idle-video voice FAQ MVP

Current first priority is Android + Gateway + ASR/TTS/LLM + small FAQ. Phase 1 does not run LiveTalking, Wav2Lip, MuseTalk, WebRTC digital-human mode or GPU inference.

Target flow:

`Android start → local idle character video → tap to consult → USB/default mic recording → Gateway upload → Doubao ASR → mini FAQ retrieval → LLM grounded answer → Doubao TTS → Android playback and subtitles → idle`

## M2 — Android kiosk and audio

Landscape immersive APK, local idle character video, endpoint configuration, device diagnostics, USB/default microphone recording and speaker playback.

## M3 — Gateway and providers

Lightweight Gateway, request IDs, sanitized logs, ASR/LLM/TTS/Knowledge Provider interfaces, Doubao ASR/TTS, configurable LLM and cost/error guards.

## M4 — Mini knowledge test

10–30 human-reviewed FAQs, simple retrieval, forbidden topics, transfer-to-human and evaluation set. No Dify and no vector database.

## M5 — End-to-end store pilot

Android → ASR → mini knowledge/LLM → TTS → playback/subtitles → idle video, with logs, fallback and privacy controls.

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
- `docs/operations/MVP_DEPLOYMENT.md`
