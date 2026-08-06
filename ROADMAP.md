# Roadmap

## M0 — Project bootstrap

Repository, environment audit, upstream lock, secret protections and Codex execution discipline.

Current gate: `TASK-000` is done. The locked LiveTalking checkout exists under ignored `third_party/LiveTalking`; see `docs/evidence/TASK-000/environment-audit.md`.

## M1 — LiveTalking reproducible baseline

Wav2Lip first; WebRTC/WHEP, `/human`, `/humanaudio`, interrupt, speaking state, record, action state and SSE verified with evidence.

## M2 — Android kiosk shell

Landscape immersive APK, WebView/WebRTC page, local idle video, endpoint configuration, automatic reconnect and device diagnostics.

## M3 — Audio hardware loop

USB microphone preference/fallback, recording, external/internal speaker playback, echo and long-run checks.

## M4 — Model adapters

Mock, EdgeTTS, Doubao TTS, Doubao ASR, Doubao/Qwen/OpenAI-compatible LLM, unified errors and cost protection.

## M5 — Mini knowledge test

10–30 reviewed FAQs, simple retrieval, forbidden topics, transfer-to-human and test set. No vector database.

## M6 — End-to-end store pilot

Android → ASR → mini knowledge/LLM → TTS → idle video or LiveTalking → logs, with fallback and privacy notice.

## M7 — Production deployment

Tencent Cloud gateway, TLS, authentication, monitoring, backup and optional separate GPU node / TURN.

## M8 — Formal knowledge base and advanced avatar

Only after pilot evidence: document workflow, vector retrieval, administration, MuseTalk evaluation and richer action orchestration.

See `docs/22_DELIVERY_BLUEPRINT.md` for the task dependency gates, evidence ladder, acceptance spine and rollback strategy used across this roadmap.
