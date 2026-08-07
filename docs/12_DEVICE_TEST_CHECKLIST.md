# Android 12 device test checklist

Mark unknown items as `PENDING`; do not infer them from marketing material.

## TASK-015 current candidate and decision

- Status: `BLOCKED / NO-GO` on 2026-08-07.
- Local TASK-014C through TASK-014G implementation, Gateway tests, Android unit/lint/build and repository validation are complete.
- Real-device validation is `PENDING` because `adb devices -l` returned no device and no Android 12 AVD is installed.
- APK for hardware test: `android-app\app\build\outputs\apk\debug\app-debug.apk`
- APK size: `6451579` bytes
- APK SHA-256: `79353D6547FF13A7415ACD00772F445E4084C301FAF3DC730859B7207627AFB5`
- This debug APK is not the formal signed candidate. Required next setup: Android 12 display, USB microphone, target speaker, approved media/Profile, trusted HTTPS and formal signed N/N+1/N+2 APKs.
- Source-side device change handling is implemented with Android `AudioDeviceCallback`; physical unplug/replug recovery remains `PENDING` until tested on the target display.

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
- [ ] Unplug/replug recovery on real USB microphone hardware.
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

## Secure content and Display Profile

- [ ] Startup performs an immediate bootstrap sync.
- [ ] Foreground change becomes visible within 75 seconds; unchanged request returns `304`.
- [ ] Offline start keeps the active cached bundle.
- [ ] Bad hash, oversize and interrupted downloads leave active unchanged.
- [ ] Decoder failure restores `previous` without a black-screen loop.
- [ ] 1080x1920 portrait fit/fill/crop, anchor/scale, subtitle safe area/font and button center visually accepted.

## Streaming ASR, VAD and interruption

- [ ] Partial subtitles appear while speaking; only final text produces one answer.
- [ ] VAD auto-stops after normal speech and silence.
- [ ] 10 interruption trials: at least 9 stop playback within 700 ms after `speech_started`; stale answer never resumes.
- [ ] 10 playback-only trials: zero false interruptions.
- [ ] AEC unavailable or echo feedback is treated as a release blocker, not silently downgraded.

## Managed kiosk and restart

- [ ] Device Owner confirmed in `dumpsys device_policy`.
- [ ] Runtime reports `managed_locked`, `permitted=true`, `locked=true`.
- [ ] Persistent Home, Home/Overview/notification restrictions manually verified.
- [ ] Process kill recovery and 10/10 reboot cycles restore cached idle state and clear unfinished dialogue.

## Signing, update and rollback release

- [ ] Formal signing-certificate SHA-256 matches the custody register.
- [ ] N to N+1 managed silent upgrade retains data and kiosk state.
- [ ] Unmanaged install displays Android confirmation through `STATUS_PENDING_USER_ACTION`.
- [ ] Wrong hash, package, certificate and non-newer version are rejected.
- [ ] Previous stable source is released as N+2 and upgrades successfully; no downgrade install is used.

## Stability and final decision

- [ ] At least 8 continuous hours with sanitized resource/error observations.
- [ ] 30 realistic consultations with request IDs and no duplicate answers.
- [ ] GO only if signing, AEC, USB audio, kiosk and rollback gates all pass; otherwise NO-GO.
