# TASK-007: Implement and validate USB/default microphone and speaker behavior

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-005
- **Branch:** `task/TASK-007-android-usb-audio`
- **Owner:** Codex / assigned developer

## Objective

Implement and validate USB/default microphone and speaker behavior.

## Preconditions

- TASK-005 is DONE
- Actual Android device access is preferred

## Scope and allowed changes

- `android-app/`
- `docs/evidence/TASK-007/`
- `docs/12_DEVICE_TEST_CHECKLIST.md`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Continuous wake-word listening

## Detailed execution

1. Enumerate Android input/output audio devices and expose a diagnostic view/log.
2. Prefer USB input when present; safely fall back to system default.
3. Implement bounded recording, cancellation and playback with lifecycle cleanup.
4. Test permission denial, no-device, unplug/replug and speaker feedback scenarios.
5. On emulator only, mark real USB compatibility as BLOCKED rather than DONE.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
adb devices -l
```
```powershell
adb shell dumpsys audio
```
```powershell
adb shell dumpsys usb
```
```powershell
.\android-app\gradlew.bat -p android-app connectedDebugAndroidTest
```

## Required deliverables

- [x] Audio device diagnostics
- [x] Recording/playback flow
- [x] Real-device or explicit blocker report

## Acceptance criteria

- [x] Audio devices enumerated in Android client source
- [x] USB preference and fallback implemented in route policy
- [x] Recording/playback flow implemented
- [x] Real-device report or explicit device blocker
- [ ] Unplug/replug recovery

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

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## TASK-007 Result

- Android client now implements runtime microphone permission, audio device diagnostics, USB-first input preference, default fallback, bounded in-memory PCM recording, playback and lifecycle cleanup.
- Evidence:
  - `docs/evidence/TASK-007/android-audio.md`
  - `docs/evidence/TASK-007/task007-gradle-first-run-20260806.txt`
  - `docs/evidence/TASK-007/task007-final-verification-20260806.txt`
  - `docs/evidence/TASK-007/task007-closeout-checks-20260806.txt`
- Local verification passed: Gradle `testDebugUnitTest assembleDebug`, `lintDebug`, repository verification and `git diff --check`.
- Debug APK SHA-256: `2770C3CC306AB3BF0CEE0F342A3B426436ACF88F602990806F9E24D5162D195F`.
- Real hardware blocker: no Android 12 device was connected. `adb devices -l` returned an empty list; `adb shell dumpsys audio` and `adb shell dumpsys usb` failed with `no devices/emulators found`.
- TASK-007 remains `PARTIAL` until a connected Android 12 display validates USB/default microphone, speaker playback and unplug/replug recovery.
