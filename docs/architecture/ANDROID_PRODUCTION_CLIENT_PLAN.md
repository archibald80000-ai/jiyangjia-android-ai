# Android Production Client Plan

- Status: Proposed
- Date: 2026-08-07
- Target: Android 12 dedicated 9:16 store display

## Objective

Move the current local-file, whole-WAV Android client to a remotely managed production client without placing Provider or admin credentials in the APK.

## Runtime Flow

```text
HTTPS bootstrap
-> read actual window metrics
-> fetch matching Display Profile and published asset manifest
-> verify version, size and SHA-256
-> atomically activate cached video/background/profile
-> poll for changes while the kiosk is active
-> keep the last known-good bundle for offline startup and rollback
```

The Android client never calls Doubao directly. Dialogue and streaming audio always pass through the Gateway so Provider keys, policy, RAG and request tracing stay server-side.

## Secure Bootstrap

- Release builds use one HTTPS bootstrap URL, supplied by a build-time non-secret setting.
- Debug builds may use a local development URL through a separate flavor; production must reject cleartext HTTP.
- `/api/v1/client/config` returns `config_version`, refresh interval, API paths, minimum client version and release metadata path.
- A revocable device token may be provisioned per screen and stored with Android Keystore-backed storage. `ADMIN_TOKEN` and Provider keys are never sent to Android.
- Configuration is accepted only after schema validation. Invalid remote data leaves the last known-good configuration active.

## Content Synchronization

- Fetch config, profile and manifest immediately on app start and network recovery.
- Poll every 60 seconds while the kiosk is foreground; use conditional requests (`ETag` / `If-None-Match`) to avoid redownloading unchanged content.
- Download to a temporary app-private file, enforce maximum size, verify content type and SHA-256, then rename atomically.
- Keep active and previous bundles. Playback or decode failure automatically restores the previous bundle and reports a sanitized diagnostic.
- WorkManager handles deferred retry after process death or connectivity restoration; it is not the low-latency foreground update channel.

## Display Rendering

Layer order:

1. background image;
2. idle character video;
3. subtitles and status;
4. consultation and diagnostic controls.

Profile behavior:

- `fit`: preserve aspect ratio and contain the full media;
- `fill`: stretch to the assigned bounds;
- `crop`: preserve aspect ratio and center-crop to cover;
- character anchor and scale use normalized profile coordinates;
- subtitle safe areas and button positions use normalized screen coordinates;
- profile selection uses actual window width, height and orientation, not a hard-coded device model.

Media3 ExoPlayer is preferred over `VideoView` for deterministic looping, scaling, decode errors and cache integration.

## Streaming Dialogue

```text
Android AudioRecord PCM frames
-> WSS Gateway session
-> Doubao bidirectional streaming ASR
-> partial transcript events
-> VAD/final transcript
-> existing normalization + RAG + LLM + TTS
-> answer metadata and audio retrieval
```

The existing multipart WAV endpoint remains the fallback. A tap during TTS must stop playback, invalidate the old response and open a new ASR stream. Automatic acoustic barge-in is accepted only after device echo-cancellation testing; tap-to-interrupt is the reliable MVP behavior.

## Managed Kiosk and Updates

- True Lock Task requires Device Owner/DPC allowlisting; ordinary immersive mode or screen pinning is not equivalent.
- Preferred deployment is a fully managed dedicated device with the kiosk app as the persistent Home activity.
- A fallback BootReceiver can restore the app after reboot, but it cannot guarantee the same control on every OEM build.
- Release APKs use one long-lived signing identity stored outside Git.
- Update metadata includes version code, URL, SHA-256 and signing-certificate digest.
- Silent installation is enabled only on a managed Device Owner path. Otherwise Android must show the system installation confirmation.
- Code rollback is released as a new, higher `versionCode` built from the previous known-good source; asset/profile rollback uses the cached previous bundle.

## Production Gates

- Trusted HTTPS endpoint and stable hostname/IP certificate strategy.
- Device provisioning decision: fully managed Device Owner or limited unmanaged mode.
- Approved 9:16 video/background assets and size limits.
- Release signing key custody and backup owner.
- Physical Android 12 hardware for USB audio, rendering, reboot and long-run acceptance.
