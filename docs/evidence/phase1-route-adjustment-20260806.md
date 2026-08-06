# Phase 1 Route Adjustment Evidence

Updated: 2026-08-06

## Decision

Phase 1 defers LiveTalking, Wav2Lip, MuseTalk, realtime lip sync, WebRTC digital-human mode and GPU inference.

Phase 1 target is Android idle character video + tap-to-talk + USB/default microphone + Gateway + Doubao ASR/TTS + LLM + 10-30 approved FAQ + subtitles.

## Files Added

- docs/architecture/MVP_ARCHITECTURE.md
- docs/architecture/ANDROID_CLIENT.md
- docs/architecture/GATEWAY_AND_PROVIDERS.md
- docs/architecture/KNOWLEDGE_MVP.md
- docs/architecture/FUTURE_LIVETALKING_UPGRADE.md
- docs/api/MVP_API_SPEC.md
- docs/testing/MVP_ACCEPTANCE.md
- docs/operations/MVP_DEPLOYMENT.md
- docs/adr/ADR-0008_PHASE1_IDLE_VIDEO_VOICE_MVP.md

## Task Route

TASK-000 -> TASK-005 -> TASK-007 -> TASK-008 -> TASK-009 -> TASK-010 -> TASK-011 -> TASK-012 -> TASK-013 -> TASK-014 -> TASK-015

Deferred: TASK-003, TASK-004, TASK-006, TASK-016.

## Safety

- No model download attempted.
- No asset preparation script modified in this route adjustment turn after the user requested design-only route adjustment.
- No APK/API/provider/device success claimed.
- Raw materials directory E:\work\积养家 was not scanned.
