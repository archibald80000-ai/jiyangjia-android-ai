# Android 12 device test checklist

Mark unknown items as `PENDING`; do not infer them from marketing material.

## TASK-007 current status

- Status: `PARTIAL`
- Local Android audio implementation, unit tests, lint and APK build are complete.
- Real-device audio validation is `PENDING` because no Android device was connected during verification on 2026-08-06.
- APK for hardware test: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- APK size: `848096` bytes
- APK SHA-256: `2770C3CC306AB3BF0CEE0F342A3B426436ACF88F602990806F9E24D5162D195F`
- Required next hardware setup: Android 12 display, USB microphone, target speaker path, ADB or install path.

## System

- [ ] Manufacturer/model/firmware recorded.
- [ ] Android 12 build number recorded.
- [ ] CPU ABI: arm64-v8a / armeabi-v7a / x86_64.
- [ ] Screen resolution, aspect ratio and refresh rate.
- [ ] Touch capability.
- [ ] Unknown-source APK installation.
- [ ] ADB/developer options.
- [ ] App auto-start / kiosk permission.
- [ ] Background process and battery restrictions.

## USB audio

- [ ] USB Host mode.
- [ ] USB microphone enumerated.
- [ ] Android reports device type as USB audio input.
- [ ] App permission granted.
- [ ] 30-second recording test.
- [ ] Sample rate/channel recorded.
- [ ] Unplug/replug recovery.
- [ ] Default microphone fallback.

## Output

- [ ] Internal speaker playback.
- [ ] External speaker playback.
- [ ] Volume control behavior.
- [ ] Feedback/echo test at operating volume.

## Network and display

- [ ] HTTPS endpoint reachable.
- [ ] WebView JavaScript/media/WHEP support.
- [ ] Local idle video loops for 2 hours.
- [ ] Wi-Fi/Ethernet disconnect and recovery.
- [ ] Navigation/status bar remains hidden.
- [ ] App recovers after reboot.
