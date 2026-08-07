# TASK-014D - Android Display Profile Renderer

- **Status:** PLANNED
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
