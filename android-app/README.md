# Android app

Android client for the public phone experience and the managed Android 12 store display. Both variants use the same real Gateway and 9:16 presentation renderer, but their device-control capabilities are intentionally different.

## Variants

| Variant | Package | Intended device | Device-control behavior |
| --- | --- | --- | --- |
| `phoneDemo` | `ai.jiyangjia.kiosk.debug` | Ordinary Android phone | Normal Home, recents, notifications and app switching; no boot receiver, Home role, Device Admin, Lock Task or package-install permission |
| `storeKiosk` | `ai.jiyangjia.kiosk.store` | Managed Android 12 store display | Home role, boot recovery, Device Owner/Lock Task, immersive mode, keep-screen-on and controlled update support |

Do not install the store-kiosk variant on an ordinary phone. It is designed for a recoverable, fully managed store device.

Current shared version:

- `versionCode=9`
- `versionName=0.1.8`
- application label: `积养家AI数字人`

## Build

Build requires JDK 17 and Android SDK platform/build tools for API 35. From the repository root:

```powershell
$env:JAVA_HOME = "<jdk-17-path>"
$env:ANDROID_HOME = "<android-sdk-path>"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
.\android-app\gradlew.bat -p android-app `
  testPhoneDemoDebugUnitTest testStoreKioskDebugUnitTest `
  lintPhoneDemoDebug lintStoreKioskDebug `
  assemblePhoneDemoDebug assembleStoreKioskDebug
```

Local outputs:

- Phone: `android-app\app\build\outputs\apk\phoneDemo\debug\app-phoneDemo-debug.apk`
- Store: `android-app\app\build\outputs\apk\storeKiosk\debug\app-storeKiosk-debug.apk`

Published debug artifacts:

- Phone: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-digital-human.apk`
- Store: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-store-kiosk.apk`
- Legacy phone alias: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-demo.apk`

These are debug-signed demonstration artifacts. Formal release signing and Android 12 managed-device update/rollback acceptance remain separate gates.

## Gateway Base URL

- Production origin: `https://ai-jiyangjia.cloud`.
- Release builds always disable cleartext Gateway traffic.
- Debug builds use the production HTTPS origin by default.
- Development may override the debug origin with `JIYANGJIA_GATEWAY_BASE_URL`.
- Local HTTP additionally requires `JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY=true`; never use it for a release build.

Example:

```powershell
$env:JIYANGJIA_GATEWAY_BASE_URL = "http://192.168.1.10:18084"
$env:JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY = "true"
.\gradlew.bat assemblePhoneDemoDebug
```

Provider credentials are server-only and must never be added to Gradle properties, `BuildConfig`, resources or APK files.
