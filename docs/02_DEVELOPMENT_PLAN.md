# Development plan

Development follows dependency order, not feature excitement.

## Phase 0 — Repository and environment

Audit tools, protect secrets, pin upstream and establish reproducible commands.

## Phase 1 — Android idle-video voice FAQ MVP

Build the Android 12 idle-video voice FAQ loop first. No LiveTalking, Wav2Lip, MuseTalk, WebRTC digital-human mode or GPU inference.

## Phase 2 — Android shell and audio

Build landscape kiosk shell, local idle character video, endpoint configuration, USB/default microphone recording and speaker playback.

## Phase 3 — Gateway and providers

Create Gateway, Provider interfaces, Doubao TTS, Doubao ASR, configurable LLM and request/log/error contracts.

## Phase 4 — Mini knowledge

Only reviewed questions and answers. Simple exact/keyword/normalized matching is sufficient. Add tests, prohibited topics and staff handoff.

## Phase 5 — End-to-end and deployment

Connect Android → Gateway → ASR → FAQ/LLM → TTS → playback/subtitles. Deploy Gateway to Tencent Cloud with TLS, device token, logs, backup and rollback.

## Phase 6 — Android device acceptance

Test on actual Android 12 display: APK install, USB mic, speaker, idle video, network recovery, reboot and long-run checks.

## Phase 7 — Future LiveTalking enhancement

Re-open LiveTalking/Wav2Lip/MuseTalk/WebRTC only after Phase 1 acceptance and GPU/runtime/assets are approved.
