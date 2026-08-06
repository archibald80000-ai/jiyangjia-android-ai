# Task index

The canonical machine-readable index is [`tasks/index.yaml`](tasks/index.yaml). Human-readable instructions are in [`tasks/README.md`](tasks/README.md).

Current status:

- `TASK-000`: `DONE`; environment/repository audit passed and LiveTalking locked checkout exists under ignored `third_party/LiveTalking`.
- `TASK-001`: `DONE`; locked LiveTalking upstream source audited with endpoint, model/asset, network, extension and compliance notes.
- `TASK-002`: `DONE`; isolated LiveTalking runtime exists under ignored `.venv\livetalking-task002`, dependencies/imports/PyTorch CUDA smoke check passed.
- `TASK-003`: `DEFERRED`; Wav2Lip/LiveTalking asset-dependent baseline is moved to a future enhancement phase and no longer blocks Phase 1.
- `TASK-004`: `DEFERRED`; LiveTalking API automation waits until the future enhancement phase.
- `TASK-005`: `PARTIAL`; Android Kotlin landscape kiosk shell, local idle-video path handling, offline fallback visual and non-secret config entry are implemented, but APK build is blocked by missing JDK 17 / Android SDK / ADB / Gradle on this machine.
- `TASK-006`: `DEFERRED`; LiveTalking display mode is deferred; local idle video is folded into TASK-005 for Phase 1.
- Next action is to finish `TASK-005` build verification after Android toolchain setup; do not advance to TASK-007 until a real Gradle build/APK result is recorded or the user explicitly changes the gate.

Current order:

Phase 1 order:

`TASK-000 → TASK-005 → TASK-007 → TASK-008 → TASK-009 → TASK-010 → TASK-011 → TASK-012 → TASK-013 → TASK-014 → TASK-015`

Future enhancement:

`TASK-003/TASK-004/TASK-006/TASK-016` for LiveTalking / Wav2Lip / MuseTalk / WebRTC digital human work.

Do not execute multiple implementation tasks concurrently unless a later task explicitly permits parallel work.
