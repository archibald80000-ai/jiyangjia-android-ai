# TASK-007 Android Audio Evidence

- **Task:** TASK-007 Android USB/default microphone and speaker behavior
- **Date:** 2026-08-06
- **Branch:** `task/TASK-007-android-usb-audio`
- **Status:** PARTIAL

## Implemented

- Added `android.permission.RECORD_AUDIO` to the Android manifest.
- Added runtime microphone permission flow in `KioskActivity`.
- Added on-screen audio diagnostics:
  - enumerates Android input devices;
  - enumerates Android output devices;
  - shows preferred input and preferred output;
  - exposes a refresh button.
- Added USB-first route policy:
  - prefers USB input device types when present;
  - falls back to the first available system input;
  - chooses a usable output device, preferring speaker/USB/wired outputs when present.
- Added bounded local recording:
  - PCM 16-bit mono;
  - 16 kHz sample rate;
  - maximum duration is clamped by existing client config, with controller cap `10` seconds;
  - recording remains in memory and is not written to disk.
- Added local playback of the captured PCM through `AudioTrack`.
- Added lifecycle cleanup for active recorder/player.
- Added Android `AudioDeviceCallback` monitoring:
  - refreshes diagnostics when audio devices are added or removed;
  - stops an active recording if the input/output device set changes;
  - returns the client to an error state with a retry prompt instead of keeping a stale recorder alive.
- Added unit tests for USB preference/fallback, diagnostics summary and PCM duration/playability.

## Verification

Full logs:

- `docs/evidence/TASK-007/task007-gradle-first-run-20260806.txt`
- `docs/evidence/TASK-007/task007-final-verification-20260806.txt`
- `docs/evidence/TASK-007/task007-closeout-checks-20260806.txt`
- `docs/evidence/TASK-007/task007-device-callback-verification-20260806.txt`

Final results:

| Check | Result |
| --- | --- |
| `adb devices -l` | No connected device. |
| `adb shell dumpsys audio` | Failed with `no devices/emulators found`. |
| `adb shell dumpsys usb` | Failed with `no devices/emulators found`. |
| `.\android-app\gradlew.bat -p android-app clean testDebugUnitTest assembleDebug lintDebug --no-daemon --stacktrace` | BUILD SUCCESSFUL. |
| `.\android-app\gradlew.bat -p android-app connectedDebugAndroidTest` | BUILD SUCCESSFUL as a Gradle task, but no connected Android 12 device was listed by ADB, so this is not real hardware validation. |
| `aapt dump badging` | APK includes `android.permission.RECORD_AUDIO` and declares microphone feature. |
| `scripts/verify_repository.ps1` | PASS. |
| `git diff --check` | PASS. |

Unit test summary:

- `AudioRoutePolicyTest`: 3 tests, 0 failures, 0 errors.
- `PcmAudioTest`: 2 tests, 0 failures, 0 errors.
- `ClientConfigTest`: 2 tests, 0 failures, 0 errors.
- `ConsultationStateTest`: 1 test, 0 failures, 0 errors.

APK:

- Path: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- Size: `849801` bytes
- SHA-256: `B2FEBA1C2E2A69D0AE2ED43DB000D75F0EA1BC67D396E9ECE22F8512A4D22D49`

## Not Verified

- Android 12 real-device install.
- USB Host support.
- USB microphone enumeration on the target display.
- Real recording from USB microphone.
- Real fallback to built-in/default microphone.
- Speaker or external speaker playback on target hardware.
- Real unplug/replug recovery on target hardware. Source-side add/remove monitoring and active-recording stop behavior are implemented, but physical USB recovery was not validated.
- Echo/feedback behavior at store volume.

## Blocker

No Android 12 display or emulator/device was connected during TASK-007 verification. `adb devices -l` returned an empty device list, and both `adb shell dumpsys audio` and `adb shell dumpsys usb` failed with `no devices/emulators found`.

## Next Action

Continue TASK-007 on a connected Android 12 display with the intended USB microphone and speaker attached. Do not move to Gateway/provider tasks until the hardware path is verified or explicitly waived.
