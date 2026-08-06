# Handoff

## Current task

- Current task: `TASK-007_ANDROID_USB_AUDIO.md`
- Status: `PARTIAL`; Android audio source/local build verified, real Android 12 USB/speaker validation pending
- Current branch: `task/TASK-007-android-usb-audio`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## Phase 1 route

As of 2026-08-06, Phase 1 is the Android idle-video voice FAQ MVP:

```text
Android start
-> local idle character video
-> tap to consult
-> USB/default microphone recording
-> Gateway upload
-> Doubao ASR
-> small approved FAQ retrieval
-> LLM grounded answer
-> Doubao TTS
-> Android playback and subtitles
-> idle
```

Do not download LiveTalking/Wav2Lip/MuseTalk models, do not continue changing asset preparation scripts, and do not treat missing LiveTalking assets as blocking Phase 1.

## Read first

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `PROJECT_STATE.md`
5. `ROADMAP.md`
6. `TASKS.md`
7. `docs/architecture/MVP_ARCHITECTURE.md`
8. `docs/architecture/ANDROID_CLIENT.md`
9. `docs/api/MVP_API_SPEC.md`
10. `docs/testing/MVP_ACCEPTANCE.md`
11. `tasks/TASK-005_ANDROID_KIOSK_SHELL.md`

## What is verified

- TASK-000 is done: repository/environment audit and secret checks passed.
- TASK-001/TASK-002 are done historically for LiveTalking upstream/runtime prep, but they are not Phase 1 blockers.
- TASK-003 was blocked by missing real Wav2Lip assets and is now `DEFERRED`.
- TASK-004 LiveTalking API automation is `DEFERRED`.
- TASK-006 LiveTalking display mode is `DEFERRED`; Phase 1 local idle video is folded into TASK-005.
- TASK-016 MuseTalk evaluation is `DEFERRED`.
- Existing Tencent Cloud server is 8C/4G/10M and has no GPU; it is suitable only for the lightweight Gateway in Phase 1.
- Android client must not store provider secrets.
- Knowledge MVP remains 10-30 human-approved FAQ entries; no Dify, vector DB or raw-material bulk scan.
- TASK-005 source implementation exists under `android-app/`: package `ai.jiyangjia.kiosk`, version `0.1.0-task005`, immersive landscape `KioskActivity`, local idle video path, offline animated fallback, long-press config dialog and state/config test sources.
- TASK-005 verification evidence exists under `docs/evidence/TASK-005/`.
- TASK-005 official Gradle Wrapper exists under `android-app/gradle/wrapper/`.
- TASK-005 local ignored toolchain cache exists under `.cache/android-toolchain` with Temurin JDK 17 and Android SDK API 35 components.
- TASK-005 Gradle `tasks`, `testDebugUnitTest assembleDebug` and `lintDebug` passed.
- TASK-005 debug APK exists at `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `830932` bytes, SHA-256 `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`.
- TASK-005 `adb devices` returned no connected device, so Android 12 install/rendering is not verified.
- Repository verification and `git diff --check` passed during TASK-005.
- TASK-007 Android client now includes runtime `RECORD_AUDIO` permission, audio diagnostics, USB-first input routing policy, bounded in-memory PCM recording and local playback.
- TASK-007 local verification passed: `testDebugUnitTest assembleDebug`, `lintDebug`, `aapt dump badging`, repository verifier and whitespace checks.
- TASK-007 unit tests: 8 total, 0 failures/errors.
- TASK-007 debug APK SHA-256: `2770C3CC306AB3BF0CEE0F342A3B426436ACF88F602990806F9E24D5162D195F`.
- TASK-007 blocker: `adb devices -l` returned no connected device; `dumpsys audio` and `dumpsys usb` could not run.

## New design documents

- `docs/architecture/MVP_ARCHITECTURE.md`
- `docs/architecture/ANDROID_CLIENT.md`
- `docs/architecture/GATEWAY_AND_PROVIDERS.md`
- `docs/architecture/KNOWLEDGE_MVP.md`
- `docs/architecture/FUTURE_LIVETALKING_UPGRADE.md`
- `docs/api/MVP_API_SPEC.md`
- `docs/testing/MVP_ACCEPTANCE.md`
- `docs/operations/MVP_DEPLOYMENT.md`
- `docs/adr/ADR-0008_PHASE1_IDLE_VIDEO_VOICE_MVP.md`

## Phase 1 task order

```text
TASK-000
-> TASK-005 Android landscape shell and local idle video
-> TASK-007 USB/default microphone and speaker
-> TASK-008 lightweight Gateway
-> TASK-009 Doubao TTS
-> TASK-010 Doubao ASR
-> TASK-011 LLM Provider
-> TASK-012 small approved FAQ
-> TASK-013 end-to-end voice FAQ loop
-> TASK-014 Tencent Cloud deployment
-> TASK-015 Android 12 device acceptance
```

## Not verified

- Android APK install on a real Android 12 device.
- Android 12 real-device display behavior.
- Real USB microphone and speaker routing.
- Gateway runtime implementation.
- Doubao ASR/TTS real credentials/API behavior.
- LLM provider real credentials/API behavior.
- Approved FAQ content.
- End-to-end voice FAQ loop.
- Tencent Cloud deployment.

## Next action

Continue exactly one next task: `TASK-007_ANDROID_USB_AUDIO.md`.

Expected TASK-007 focus:

- install or open the TASK-007 APK on Android 12 display;
- grant microphone permission;
- capture audio diagnostics screen/log;
- verify USB/default input diagnostics and fallback;
- run short local recording/playback smoke path;
- test speaker playback path;
- unplug/replug USB microphone and record recovery behavior;
- evidence that distinguishes emulator/no-device/local-only from real Android 12 hardware.

Do not start TASK-008 Gateway in the same task. Do not resume TASK-003/004/006/016 in Phase 1.
