# TASK-014D - Android Display Profile Renderer

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-014C DONE
- **Allowed scope:** Android rendering/media/UI modules and display tests

## Goal

Apply server Display Profiles to the real Android presentation instead of merely storing profile metadata.

## Deliverables

- Layered background, character video, subtitles and controls.
- Media3-based looping playback and decode diagnostics.
- Working `fit`, `fill` and `crop` behavior.
- Normalized character anchor/scale, subtitle safe area/font and button position.
- Runtime profile switch without activity restart or visible blank frame.
- 1080x1920 portrait default plus retained custom/landscape support.

## Acceptance

- Screenshot/pixel checks pass for 1080x1920, 1920x1080, 1280x720 and one custom profile.
- No media distortion in fit/crop modes and no text/control overlap.
- Invalid media falls back and records the failed asset version.
- Profile updates switch atomically and can roll back.
- Physical-screen visual acceptance remains TASK-015.

## Implementation result (2026-08-07)

- Media3 ExoPlayer now renders cached character video over an optional background layer, with subtitle/status and control layers above it.
- `fit`, `fill`, and centered `crop` mappings plus normalized character anchor/scale, subtitle safe-area/font size, and button-center geometry are implemented.
- A replacement player stays transparent until its first rendered frame, then atomically replaces and releases the prior player without restarting the Activity.
- Media decode failure records the failed bundle and requests TASK-014C rollback; absence of a previous bundle now returns the offline fallback instead of retrying the failed active bundle.
- Geometry unit tests cover 1080x1920, 1920x1080, 1280x720, and a custom 1600x900 profile. Android unit tests, lint, and debug assembly pass.
- Screenshot/pixel baselines and physical-screen visual acceptance remain unverified without an Android display and approved production media, so this task is not `DONE`.
