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

Current Demo build (`TASK-014H`, debug signing):

- APK: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- Size: `6,451,723` bytes
- SHA-256: `C18EE46E93153E925B807E48D72BB7A8D66865C1247794B19B4DAA098D7B396E`
- Target download URL: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-demo.apk`

The server-local HTTPS download is verified. Public browser download remains blocked until Tencent HTTPS access propagation completes. This debug APK is for Demo installation only and is not the formally signed production release required by TASK-015.

## Gateway Base URL

- Production release origin: `https://ai-jiyangjia.cloud`.
- Release builds always disable cleartext Gateway traffic.
- Debug builds use the same HTTPS origin by default.
- A developer may override debug only with Gradle property or environment variable `JIYANGJIA_GATEWAY_BASE_URL`.
- Local HTTP debug additionally requires `JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY=true`; never use this for a release build.

Example local debug override:

```powershell
$env:JIYANGJIA_GATEWAY_BASE_URL = "http://192.168.1.10:18084"
$env:JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY = "true"
.\gradlew.bat assembleDebug
```

Provider credentials are server-only and must never be added to Gradle properties, BuildConfig or APK resources.
