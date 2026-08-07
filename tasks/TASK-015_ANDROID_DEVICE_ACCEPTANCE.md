# TASK-015: Validate the actual Android 12 display in the store

- **Status:** BLOCKED
- **Priority:** P0
- **Dependencies:** TASK-014C through TASK-014G implemented locally; their physical/formal gates remain open
- **Branch:** `task/TASK-015-android-device-acceptance`
- **Owner:** Codex / assigned developer

## Objective

Validate the actual Android 12 display in the store.

## Preconditions

- TASK-014C through TASK-014G local verification is complete
- Physical Android 12 device, approved media, trusted HTTPS release hosting and formal signing identity are available

## Scope and allowed changes

- Android fixes within scope
- `docs/12_DEVICE_TEST_CHECKLIST.md`
- `docs/evidence/TASK-015/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Assuming unsupported hardware works

## Detailed execution

1. Record exact device/firmware/ABI/display/network/audio hardware.
2. Install the signed/debug candidate via the approved sideload path and record checksum.
3. Run USB mic, speaker, synchronized 9:16 media/Profile, streaming ASR/VAD/interruption, Gateway voice FAQ loop, network recovery, reboot, Lock Task and signed update tests.
4. Run a long-duration test and 30 realistic conversations in the store environment.
5. Classify defects by release blocker/severity and issue a signed acceptance decision; do not hide failed cases.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
adb devices -l
```
```powershell
adb install -r <apk>
```
```powershell
adb shell dumpsys package <package>
```
```powershell
adb logcat -d > <sanitized-log>
```

## Required deliverables

- [ ] Completed device checklist
- [ ] Installation and long-run evidence
- [ ] GO / NO-GO acceptance report

## Acceptance criteria

- [ ] APK installation
- [ ] USB microphone
- [ ] Speaker
- [ ] Network recovery
- [ ] Reboot/long-run test
- [ ] Remote asset/Profile synchronization and rollback
- [ ] Streaming ASR/VAD and playback interruption
- [ ] Lock Task/limited-mode evidence
- [ ] Signed update and rollback-release evidence
- [ ] Signed acceptance report

## Stop / blocked conditions

- A destructive change, secret exposure, uncontrolled paid call or public network exposure would be required.
- A dependency is absent and cannot be safely installed inside the authorized scope.
- Real hardware/model/provider evidence is required but unavailable.
- Existing unrelated changes make safe staging impossible.

When blocked, complete all safe analysis, save sanitized evidence, set status to `BLOCKED` or `PARTIAL`, and state the exact unblock action.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Changed files and `git diff --stat`.
- Sanitized logs/screenshots where meaningful.
- Artifact paths and SHA-256 for APK/packages.
- Hardware/environment details for device/GPU claims.
- Failed cases, untested paths and cost-bearing calls.

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [ ] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [ ] Add evidence links/results to this task.
- [ ] Update `PROJECT_STATE.md`.
- [ ] Update `memory/CURRENT_STATE.md`.
- [ ] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [ ] Recommend exactly one next task.

## Current acceptance decision (2026-08-07)

**NO-GO / BLOCKED.** `adb devices -l` returned no device, and the project-local SDK has no emulator executable or Android 12 system image. Approved media, trusted HTTPS release hosting and a formal signing identity/custody record are also absent. No hardware, Lock Task, USB audio, AEC, reboot, silent-upgrade, long-run or 30-consultation result is claimed.

Local preflight is complete: Gateway regression passed 63 tests, Android unit/lint/debug assembly passed, repository verification passed, and the current debug APK is recorded in `docs/evidence/TASK-015/task015-no-go-20260807.md`. Resume this same task when all external gates are present.
