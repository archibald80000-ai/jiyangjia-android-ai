# Android app

Phase 1 Android 12 portrait kiosk client, defaulting to a 9:16 display profile.

TASK-005 scope:

- native Kotlin app;
- immersive 9:16 portrait shell with server-side profiles retained for other screen layouts;
- local idle character video when a rights-clear file is configured;
- offline animated fallback visual when no local video is available;
- non-secret development config via long-pressing the status text;
- no provider API keys, model weights, LiveTalking runtime or raw business data in the APK.

## Build

Build requires JDK 17 and Android SDK platform/build tools for API 35. The official Gradle Wrapper is committed, so a global Gradle installation is not required after the first verified setup.

Example from the repository root:

```powershell
$env:JAVA_HOME = "<jdk-17-path>"
$env:ANDROID_HOME = "<android-sdk-path>"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
.\android-app\gradlew.bat -p android-app testDebugUnitTest assembleDebug
```

TASK-005 verified output:

- Debug APK: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- SHA-256: `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`

Android 12 device installation and rendering remain separate acceptance work.
