# TASK-014D local verification — 2026-08-07

## Implemented

- Media3 ExoPlayer layered renderer for background, character video, subtitles/status and controls.
- Profile-driven fit/fill/crop, character anchor/scale, subtitle safe area/font size and normalized button center.
- First-frame replacement keeps the previous player visible until the next asset renders.
- Decode errors identify the bundle version and call the content-bundle rollback path.
- Geometry coverage: 1080x1920, 1920x1080, 1280x720 and custom 1600x900.

## Commands and result

```powershell
$env:JAVA_HOME=(Resolve-Path '..\.cache\android-toolchain\jdk17\jdk-17.0.20+8').Path
$env:ANDROID_HOME=(Resolve-Path '..\.cache\android-toolchain\android-sdk').Path
$env:GRADLE_USER_HOME=(Resolve-Path '..\.cache\android-toolchain\gradle-user-home').Path
.\gradlew.bat testDebugUnitTest lintDebug assembleDebug
```

Result: exit code 0, `BUILD SUCCESSFUL`, 51 actionable tasks.

## Unverified gates

- No approved production MP4/background bundle was supplied.
- No Android 12 physical display is connected, so screenshot/pixel baselines, decoder compatibility and visible black-frame behavior are not claimed.
- Status remains `PARTIAL`.
