# Android Client Architecture

Updated: 2026-08-06

## Scope

Phase 1 Android is a native Android 12 landscape kiosk app for:

- local idle character video loop;
- tap-to-talk consultation;
- USB/default microphone recording;
- server upload;
- audio playback;
- subtitles and simple status display.

It does not run LiveTalking, Python, CUDA, model weights, provider SDK secrets or local LLMs.

## Main Modules

- `KioskActivity`: immersive landscape entry point, lifecycle and screen keep-awake.
- `IdleVideoController`: local video loop, fallback image, no network dependency.
- `ConsultationStateMachine`: UI state transitions and command gating.
- `AudioInputController`: microphone permission, USB/default device preference, bounded recording.
- `AudioOutputController`: TTS playback, speaker route observation and playback lifecycle.
- `GatewayClient`: authenticated HTTPS calls, request IDs, timeout/retry policy.
- `SubtitleRenderer`: transcript, answer and error text.
- `DeviceDiagnostics`: device model, Android version, ABI, display, audio devices and network status.
- `ConfigStore`: non-secret endpoint/device config.

## Local Assets

- Idle character video is local and provisioned as a non-secret media asset.
- APK may contain a low-size default idle video or placeholder only if rights are clear.
- Larger production idle videos can be copied to app-private storage or a documented external path during installation.
- The app must keep showing video/fallback visuals when Gateway is unavailable.

## Audio Rules

- User starts recording by tapping a visible button.
- No always-on listening in Phase 1.
- Prefer USB input when Android reports a usable input device.
- Fall back to default microphone with visible/logged diagnostic status.
- Apply max duration and max file size before upload.
- Delete temporary recording after request completion unless a test explicitly preserves sanitized evidence.

## State Machine

```text
BOOT
-> IDLE_VIDEO
-> REQUESTING_MIC_PERMISSION
-> READY_TO_RECORD
-> RECORDING
-> UPLOADING
-> WAITING_FOR_ASR_LLM_TTS
-> PLAYING_ANSWER
-> IDLE_VIDEO
```

Error transitions:

- permission denied -> `ERROR_MIC_PERMISSION` -> idle with retry action;
- no input device -> `ERROR_AUDIO_INPUT` -> idle with diagnostic;
- network timeout -> `ERROR_NETWORK` -> idle;
- provider/server error -> `ERROR_SERVICE` -> idle;
- playback failure -> `ERROR_AUDIO_OUTPUT` -> idle.

## Configuration

Client config is non-secret:

- Gateway base URL;
- device ID or store display ID;
- display mode: `idle_video_voice`;
- recording duration/size limit;
- video asset path/version;
- optional diagnostic flag.

Secrets remain server-side. Android may store only a revocable device token or mTLS material if a deployment task approves it.

## Phase 1 Acceptance

- Debug APK builds when Android SDK/Gradle are available.
- App launches landscape immersive.
- Idle video/fallback is visible without network.
- Recording and playback work on emulator or actual device; real USB support requires device evidence.
- Gateway request and response are rendered with transcript, answer subtitle and audio playback.
