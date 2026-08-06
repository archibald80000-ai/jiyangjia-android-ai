# Handoff

## Current task

- Current task: `TASK-005_ANDROID_KIOSK_SHELL.md`
- Status: route updated; TASK-005 is next and remains `PLANNED`
- Current branch: `task/TASK-003-wav2lip-webrtc-baseline`
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

- Android APK build/install.
- Android 12 real-device display behavior.
- USB microphone and speaker routing.
- Gateway runtime implementation.
- Doubao ASR/TTS real credentials/API behavior.
- LLM provider real credentials/API behavior.
- Approved FAQ content.
- End-to-end voice FAQ loop.
- Tencent Cloud deployment.

## Next action

Execute exactly one next task: `TASK-005_ANDROID_KIOSK_SHELL.md`.

Expected TASK-005 focus:

- create Android 12 landscape kiosk shell;
- implement local idle character video or rights-clear fallback visual;
- add non-secret endpoint/config screen;
- build/smoke-test if SDK/Gradle are available;
- save evidence and update task state.

Do not start TASK-007/008 in the same task. Do not resume TASK-003/004/006/016 in Phase 1.
