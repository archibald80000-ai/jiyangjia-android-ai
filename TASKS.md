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
- `TASK-007`: `PARTIAL`; Android runtime microphone permission, device diagnostics, USB-first input preference, bounded in-memory recording and local playback are implemented and locally built/tested, but real Android 12 USB microphone/speaker/unplug recovery validation is blocked by no connected device.
- Next action is to continue `TASK-007` on a connected Android 12 display with the intended USB microphone and speaker. Do not start Gateway/provider work until this hardware gate is verified or explicitly waived.

Current order:

Phase 1 order:

`TASK-000 → TASK-005 → TASK-007 → TASK-008 → TASK-009 → TASK-010 → TASK-011 → TASK-012 → TASK-013 → TASK-014 → TASK-015`

Future enhancement:

`TASK-003/TASK-004/TASK-006/TASK-016` for LiveTalking / Wav2Lip / MuseTalk / WebRTC digital human work.

Do not execute multiple implementation tasks concurrently unless a later task explicitly permits parallel work.
