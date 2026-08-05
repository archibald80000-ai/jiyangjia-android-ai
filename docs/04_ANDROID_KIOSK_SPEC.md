# Android kiosk specification

## Platform

- Android 12.
- Landscape and immersive full screen.
- APK sideload through USB is expected but must be verified.
- V1 recommended implementation: native Kotlin shell + WebView/WebRTC/WHEP page.

## Required modules

- `KioskActivity` / UI state container.
- Configuration manager.
- Network and health monitor.
- Local idle-video player.
- LiveTalking WebView controller.
- Audio device enumerator and recorder.
- Audio playback manager.
- Dialogue coordinator.
- Telemetry/error reporter.

## Audio behavior

- Ask for `RECORD_AUDIO` only when needed.
- Enumerate `AudioDeviceInfo`; prefer USB input if present.
- Fall back to default input safely.
- Do not assume a specific sample rate; detect/convert according to the selected ASR contract.
- Pause or duck local media audio while answer speech plays.
- Document echo-cancellation limitations of the hardware.

## Screen behavior

- Never show a blank screen during reconnect.
- Local idle video is packaged or provisioned on device.
- Subtitles show recognized text and answer text without revealing diagnostics.
- Admin configuration is protected and hidden from normal customers.

## Device acceptance

See `docs/12_DEVICE_TEST_CHECKLIST.md`. Every hardware capability marked unknown remains a blocker for production claims.
