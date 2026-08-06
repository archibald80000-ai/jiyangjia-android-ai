# TASK-005 Android Shell Evidence

- **Task:** TASK-005 Android 12 landscape kiosk shell and local idle video
- **Date:** 2026-08-06
- **Branch:** `task/TASK-005-android-kiosk-shell`
- **Status:** PARTIAL

## Implemented

- Created a native Kotlin Android application under `android-app/`.
- Package ID: `ai.jiyangjia.kiosk`.
- Version: `0.1.0-task005`, versionCode `1`.
- Implemented a landscape `KioskActivity` with immersive fullscreen mode and keep-screen-on behavior.
- Implemented local idle media resolution:
  - first uses a configured local video file path;
  - then tries an optional packaged raw resource named `idle_placeholder`;
  - then falls back to an offline animated canvas view.
- Added a long-press development configuration dialog for Gateway URL, device ID and idle video path.
- Added a first-pass client state model for `BOOT`, `IDLE_VIDEO`, `READY_TO_RECORD`, `RECORDING`, `UPLOADING`, `WAITING_FOR_RESPONSE`, `PLAYING_ANSWER` and `ERROR`.
- Added unit test sources for configuration defaults/clamping and state transition eligibility.
- No provider credentials, API keys, model weights, APKs, recordings or raw business materials were added.

## Verification Commands

Full command output is recorded in:

- `docs/evidence/TASK-005/task005-verification-20260806.txt`
- `docs/evidence/TASK-005/task005-environment-20260806.txt`
- `docs/evidence/TASK-005/task005-final-checks-20260806.txt`

Summary:

| Command | Result |
| --- | --- |
| `java -version` | Found Java `9.0.1`; Android Gradle Plugin requires JDK 17 for this project. |
| `adb version` | Failed; `adb` is not on PATH. |
| `.\android-app\gradlew.bat -p android-app tasks` | Failed; Gradle is not installed or not on PATH. |
| `.\android-app\gradlew.bat -p android-app assembleDebug` | Failed; Gradle is not installed or not on PATH. |
| `Get-FileHash android-app\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256` | APK path does not exist because build could not run. |
| `powershell -ExecutionPolicy Bypass -File .\scripts\verify_repository.ps1` | PASS. |
| `git diff --check` | PASS. |

Final checks also confirmed no APK/AAB/keystore/model/audio/video files under `android-app/`. The secret-pattern scan only matched branch names, documentation text and the non-secret default device ID.

## Environment Findings

- `JAVA_HOME` points to `D:\java\jre-1.8`.
- `java` on PATH resolves to Java `9.0.1`.
- `ANDROID_HOME` is unset.
- `ANDROID_SDK_ROOT` is unset.
- `C:\Users\Assert\AppData\Local\Android\Sdk` does not exist.
- `gradle` is not on PATH.
- `adb` is not on PATH.

## Not Verified

- Gradle build.
- Unit test execution.
- Debug APK generation.
- APK SHA-256.
- Android 12 install.
- Real idle video rendering on target display.
- Real fallback visual rendering on target display.
- Kiosk behavior under target display resolution.

## Blocker / Unblock Action

TASK-005 cannot be closed as DONE on this machine until the Android build toolchain is installed or provided:

1. JDK 17 configured for Gradle.
2. Android SDK with platform and build tools for compileSdk 35, or a documented approved compileSdk adjustment.
3. Android platform-tools with `adb`.
4. Gradle installed or an official Gradle wrapper generated and committed after verification.

After toolchain setup, rerun:

```powershell
.\android-app\gradlew.bat -p android-app tasks
.\android-app\gradlew.bat -p android-app testDebugUnitTest assembleDebug
Get-FileHash android-app\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```
