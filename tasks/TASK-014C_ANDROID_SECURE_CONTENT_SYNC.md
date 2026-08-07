# TASK-014C - Android Secure Config and Content Sync

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-014A DONE, TASK-014B DONE, production HTTPS gate supplied by deployment owner
- **Allowed scope:** Android config/cache/network modules, client config/manifest/profile read APIs, tests and evidence

## Goal

Automatically synchronize published server configuration, Display Profile, idle video and background image to Android while preserving offline startup and rollback.

## Deliverables

- Versioned client bootstrap contract with refresh interval and minimum client version.
- Android HTTPS client for config, manifest and profile selection using actual window metrics.
- ETag-aware foreground polling and connectivity-triggered refresh.
- App-private atomic asset cache with size/type/SHA-256 verification.
- Active plus previous bundle, playback-failure rollback and local fallback.
- Debug-only local endpoint support; release builds reject cleartext HTTP.

## Acceptance

- Publishing a new server asset/profile appears on a connected test client without reinstalling the APK.
- Unchanged content is not downloaded again.
- Bad hash, partial download, invalid JSON and HTTP failure retain the last known-good display.
- Process restart and network loss continue to show cached media.
- No Provider/Admin secret exists in APK, logs or cached config.

## Stop Conditions

- The deployment owner has not supplied a trusted HTTPS endpoint for production acceptance.
- Another thread is modifying the same Android config/cache files.
- Formal media exceeds an agreed size or has unknown rights.

## Implementation result (2026-08-07)

- Gateway bootstrap, stable ETag/304, asset size/SHA metadata and immutable asset responses are implemented.
- Android app-private staging, size/type/SHA-256 validation, active/previous pointers, offline cache, foreground polling, connectivity refresh and WorkManager recovery are implemented.
- Debug cleartext is isolated to the debug build; release runtime rejects non-HTTPS Gateway and asset URLs.
- Local Gateway tests and Android unit/lint/debug APK build pass.
- Trusted production HTTPS, approved media and Android 12 runtime synchronization remain unverified, so this task is not marked DONE.
