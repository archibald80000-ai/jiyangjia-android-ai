# ADR-0008: Phase 1 Idle-Video Voice FAQ MVP

Date: 2026-08-06

## Status

Accepted

## Context

TASK-003 was blocked by missing real LiveTalking/Wav2Lip model and avatar assets. Continuing to make model installation scripts more elaborate does not move the store-ready Android MVP forward. The target deployment server has no GPU, and the Android 12 large display should not run Python/CUDA/model inference locally.

## Decision

Phase 1 will not depend on LiveTalking, Wav2Lip, MuseTalk, realtime lip sync, WebRTC digital-human mode or GPU inference.

Phase 1 will deliver:

```text
Android idle character video
-> tap-to-talk recording
-> Gateway
-> Doubao ASR
-> mini FAQ retrieval
-> LLM grounded answer
-> Doubao TTS
-> Android playback and subtitles
```

LiveTalking remains a deferred enhancement. Existing LiveTalking docs, scripts, evidence and upstream checkout are retained but no longer block Phase 1.

## Consequences

- Current first implementation task becomes TASK-005.
- TASK-003, TASK-004, TASK-006 and TASK-016 are deferred until after the Phase 1 MVP.
- Gateway/provider/FAQ tasks become first-priority alongside Android audio and idle video.
- The system still keeps `DisplayMode` and provider interfaces compatible with future LiveTalking integration.

## Evidence

- `docs/architecture/MVP_ARCHITECTURE.md`
- `docs/architecture/FUTURE_LIVETALKING_UPGRADE.md`
- `docs/api/MVP_API_SPEC.md`
- `docs/testing/MVP_ACCEPTANCE.md`
