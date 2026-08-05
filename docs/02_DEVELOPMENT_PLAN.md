# Development plan

Development follows dependency order, not feature excitement.

## Phase 0 — Repository and environment

Audit tools, protect secrets, pin upstream and establish reproducible commands.

## Phase 1 — LiveTalking baseline

Use Wav2Lip first. Verify official web page, WHEP/WebRTC, text/audio drive, interrupt, state, recording, action state and SSE. Record FPS/latency only when real inference runs.

## Phase 2 — Android shell

Build landscape kiosk shell, local idle video, WebView/WHEP page, endpoint configuration, mode switch and reconnection. Do not yet add every provider.

## Phase 3 — Hardware audio

Request permission, enumerate input devices, prefer USB audio, record/play test samples, evaluate feedback and long-running behavior.

## Phase 4 — Gateway and providers

Mock end-to-end first, then EdgeTTS, Doubao TTS, Doubao ASR and one LLM. Provider failures must use unified errors and cost guards.

## Phase 5 — Mini knowledge

Only reviewed questions and answers. Simple exact/keyword/normalized matching is sufficient. Add tests, prohibited topics and staff handoff.

## Phase 6 — Deployment and pilot

Deploy gateway to Tencent Cloud, configure TLS and device token, then test with the actual Android screen and optional GPU node.

## Phase 7 — Expansion

Evaluate formal RAG, admin UI, MuseTalk, richer actions and multi-store support only after pilot evidence.
