# TASK-005 Android Shell Evidence

- **Task:** TASK-005 Android 12 landscape kiosk shell and local idle video
- **Date:** 2026-08-06
- **Branch:** `task/TASK-005-android-kiosk-shell`
- **Status:** DONE for local build/APK generation; Android 12 real-device acceptance not claimed

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
- Generated and committed the official Gradle Wrapper for Gradle `8.10.2`.
- Built a debug APK with JDK 17 and Android SDK API 35 from local ignored toolchain cache.
- No provider credentials, API keys, model weights, recordings or raw business materials were added.

## Verification Commands

Full command output is recorded in:

- `docs/evidence/TASK-005/task005-verification-20260806.txt`
- `docs/evidence/TASK-005/task005-environment-20260806.txt`
- `docs/evidence/TASK-005/task005-final-checks-20260806.txt`
- `docs/evidence/TASK-005/task005-toolchain-install-20260806.txt`
- `docs/evidence/TASK-005/task005-gradle-build-20260806.txt`
- `docs/evidence/TASK-005/task005-lint-20260806.txt`
- `docs/evidence/TASK-005/task005-final-apk-verification-20260806.txt`
- `docs/evidence/TASK-005/task005-closeout-checks-20260806.txt`

Summary:

| Command | Result |
| --- | --- |
| Initial `java -version` | Found Java `9.0.1`; insufficient for Android build. |
| Initial `adb version` | Failed; `adb` was not on PATH before local toolchain setup. |
| Local JDK 17 | Installed in ignored `.cache/android-toolchain`; `java -version` reports Temurin `17.0.20+8`. |
| Local Android SDK | Installed command-line tools, platform-tools, `platforms;android-35`, `build-tools;35.0.0`; `adb version` reports `37.0.1-15733141`. |
| Gradle Wrapper | Generated official Gradle Wrapper for `8.10.2`. |
| `.\android-app\gradlew.bat -p android-app tasks` | BUILD SUCCESSFUL. |
| `.\android-app\gradlew.bat -p android-app testDebugUnitTest assembleDebug` | BUILD SUCCESSFUL; 3 unit tests passed; APK generated. |
| `.\android-app\gradlew.bat -p android-app lintDebug` | BUILD SUCCESSFUL; lint report generated. |
| `aapt dump badging` | APK package `ai.jiyangjia.kiosk.debug`, minSdk `23`, targetSdk `35`, launch activity `ai.jiyangjia.kiosk.KioskActivity`, landscape feature present. |
| `powershell -ExecutionPolicy Bypass -File .\scripts\verify_repository.ps1` | PASS. |
| `git diff --check` | PASS. |

Final checks confirmed the APK remains in ignored build output and was not staged as a source artifact. The secret-pattern scan only matched branch names, documentation text and the non-secret default device ID.

## APK

- Path: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- Size: `830932` bytes
- SHA-256: `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`

## Environment Findings

- `JAVA_HOME` points to `D:\java\jre-1.8`.
- `java` on PATH resolves to Java `9.0.1`.
- `ANDROID_HOME` is unset.
- `ANDROID_SDK_ROOT` is unset.
- `C:\Users\Assert\AppData\Local\Android\Sdk` does not exist.
- `gradle` is not on PATH.
- `adb` is not on PATH.

## Still Not Verified

- Android 12 install.
- Real idle video rendering on target display.
- Real fallback visual rendering on target display.
- Kiosk behavior under target display resolution.

## Rebuild Command

```powershell
$env:JAVA_HOME = "E:\work\ai-kefu\jiyangjia-ai\.cache\android-toolchain\jdk17\jdk-17.0.20+8"
$env:ANDROID_HOME = "E:\work\ai-kefu\jiyangjia-ai\.cache\android-toolchain\android-sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
.\android-app\gradlew.bat -p android-app tasks
.\android-app\gradlew.bat -p android-app testDebugUnitTest assembleDebug
Get-FileHash android-app\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```

The local `.cache/android-toolchain` directory is ignored and is not committed.
