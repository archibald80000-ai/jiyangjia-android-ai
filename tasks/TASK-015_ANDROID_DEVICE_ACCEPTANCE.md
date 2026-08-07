# TASK-015: Validate the actual Android 12 display in the store

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-014G DONE
- **Branch:** `task/TASK-015-android-device-acceptance`
- **Owner:** Codex / assigned developer

## Objective

Validate the actual Android 12 display in the store.

## Preconditions

- TASK-013 and TASK-014 are DONE
- Physical device and store network are available

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
