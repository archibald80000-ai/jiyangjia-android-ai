# TASK-015B - Public Realtime Voice and Phone-safe APK

- **Status:** PARTIAL / PUBLIC_STREAM_AND_PHONE_NAV_PASS
- **Priority:** P0
- **Dependencies:** TASK-014H DONE, TASK-015 Android 13 smoke evidence
- **Branch:** `codex/TASK-015B-public-voice-phone-mode`

## Goal

Restore the public browser streaming-ASR dialogue and separate the public phone experience from the managed Android store kiosk.

## Acceptance

- Browser WebSocket start events use a non-negative integer generation and malformed starts return `INVALID_START`.
- Public `/` serves the navigable dialogue experience; `/demo/kiosk` remains a clean full-screen store view.
- Manual stop and speech-first three-second silence submission reach ASR, RAG, LLM and TTS with visible transcript, sources and audio playback.
- The public phone APK retains package `ai.jiyangjia.kiosk.debug` for in-place upgrade and does not declare Home, boot, Device Admin or package-install capabilities.
- The separate store APK retains managed Home, boot, Device Owner and Lock Task behavior.
- Version is `9` / `0.1.8`; both APKs pass build, package and signature inspection.
- Production changes are backed up, narrowly deployed and publicly verified before this task is marked DONE.

## Boundaries

- Do not modify Provider, RAG or knowledge behavior.
- Do not claim Android 12 store-device acceptance from phone or browser checks.
- Do not commit APKs, secrets, recordings, SQLite, FAISS or rights-sensitive media.
- LiveTalking, Wav2Lip, MuseTalk and GPU inference remain deferred.

## Rollback

Restore the backed-up Nginx locations, previous Gateway image and previous public APK. Keep TASK-015 PARTIAL until the Android 12 store-screen gates pass.

## Result (2026-08-12)

- Public `/` and `/demo/kiosk` are online with separate navigation behavior and `Permissions-Policy: microphone=(self)`.
- Invalid string generations return `INVALID_START`. A real production WebSocket request for `积养家是什么？` returned Doubao partial/final ASR, three approved sources, an answering heartbeat and Doubao TTS audio.
- Phone and store APKs build as version `9` / `0.1.8`; the phone package has no Home, custom boot, Device Admin or package-install declarations.
- The public phone APK passed three cold launches and Home/recents/notification navigation on the connected Xiaomi Android 13 device with no fatal exception.
- Connected instrumentation could not run because MIUI rejected the test APK with `INSTALL_FAILED_USER_RESTRICTED`. That failed test install removed the app, and reinstall requires the user to approve USB installation on the unlocked device.
- Human browser-microphone speech remains a manual acceptance item. TASK-015 remains PARTIAL for Android 12 USB/store-kiosk acceptance.

Evidence: `docs/evidence/TASK-015B/task015b-public-voice-phone-mode-20260812.md`.
