# ADR-0013: Fully Managed Device and Automatic Acoustic Barge-in

- Status: Accepted
- Date: 2026-08-07

## Decision

The target Android 12 display may be factory-reset and provisioned as a fully managed Device Owner. True Lock Task, persistent Home and silent update acceptance therefore use the managed route; unmanaged immersive mode remains a clearly labeled recovery/development mode only.

Automatic acoustic interruption is a Phase 1 release requirement. The client listens through `VOICE_COMMUNICATION` with AEC/noise suppression during answer playback and stops the old generation on Gateway `speech_started`. The button remains a fallback control, not a substitute acceptance mode.

## Consequences

- Missing/ineffective AEC, repeated speaker echo triggers or failure to meet the 9/10 under-700 ms criterion blocks release.
- Device Owner, Lock Task and silent installation must be verified from Android system state after provisioning; code presence is insufficient.
- TASK-015 cannot issue GO without the physical device, USB/speaker setup and formal signed releases.
