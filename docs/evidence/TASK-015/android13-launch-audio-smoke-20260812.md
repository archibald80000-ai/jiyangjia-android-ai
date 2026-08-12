# TASK-015 Android 13 launch and audio smoke

Date: 2026-08-12

## Result

`PARTIAL / ANDROID_13_SMOKE_PASS`. The startup crash and built-in microphone dialogue path were repaired and verified on a connected Xiaomi Android 13 phone. This result does not satisfy the Android 12 store-screen acceptance gate.

## Android changes

- Immersive mode is applied only after the decor view exists and degrades without crashing when the insets controller is unavailable.
- Recording uses a real microphone source and reports captured PCM bytes/duration.
- Manual end/send and speech-first three-second silence auto-send both enter the same upload path.
- Streaming fallback generation/cancellation no longer leaves the UI stuck after recording.
- The app has a branded adaptive launcher icon.
- App/display name: `积养家AI数字人`.
- Debug version: `versionCode=8`, `versionName=0.1.7-demo-debug`, package `ai.jiyangjia.kiosk.debug`.

## Real phone smoke

- Captured built-in microphone PCM: 232,000 bytes over about 7,250 ms.
- Three seconds of silence ended the recording automatically.
- Real ASR normalized the spoken brand question to `请问积养家是什么？`.
- RAG returned approved sources `品牌名称含义` and `品牌定位——积养家是做什么的`.
- Real LLM answer appeared as subtitles.
- Doubao TTS played through the phone speaker at 24 kHz and the client returned to IDLE.
- No raw phone recording is retained in Git.

## Automated checks

```text
Gateway pytest: 111 passed
Android testDebugUnitTest + lintDebug + assembleDebug: BUILD SUCCESSFUL
connectedDebugAndroidTest: blocked by MIUI INSTALL_FAILED_USER_RESTRICTED; zero instrumentation assertions ran
```

The MIUI installation policy result is recorded as a device-policy limitation, not a passed instrumentation run.

## APK publication

- Public URL: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-digital-human.apk` (the old `jiyangjia-ai-demo.apk` URL remains compatible).
- Download filename: `积养家AI数字人.apk` via UTF-8 Content-Disposition.
- Size: 6,386,815 bytes.
- SHA-256: `65E5F031FE807094DC0CD6D85D560A64818A3CC5BF8DF2F9F9228604E70EE0FD`.
- APK signature verification: v1 and v2 schemes pass; current artifact uses the existing Android Debug certificate.
- Server backup: `/opt/jiyangjia-ai/backups/task015-apk-v8-20260812/`.
- Public re-download: HTTP 200; byte count and SHA-256 match the v8 local build. The response advertises UTF-8 filename `积养家AI数字人.apk`.

## Remaining Android 12 gates

- USB microphone selection, unplug/replug and fallback.
- External speaker routing and acoustic feedback behavior.
- 9:16 Profile rendering on the actual display.
- reboot/autostart, Device Owner Lock Task and offline recovery.
- formal production signing/update rollback and long-run stability.
