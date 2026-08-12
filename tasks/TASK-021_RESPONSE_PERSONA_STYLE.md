# TASK-021: Grounded response persona and conversational style

Status: `DONE / PRODUCTION_PUBLISHED`

## Goal

Make approved-knowledge answers sound like a warm, lively 积养家 neighbourhood guide without changing knowledge facts, relaxing draft isolation or inventing prices, inventory, activity status or medical effects.

## Delivered

- Added versioned persona `jiyangjia-neighbor-guide-v1` with concise, story and choice response modes.
- Rewrites story and gift-selection queries for retrieval while preserving the original customer intent for response metadata.
- Hydrates up to two approved matched chunks for answer generation; public search responses remain bounded and unchanged.
- Disables Doubao deep thinking for real-time Chat API requests and uses a bounded story generation budget.
- Applies natural Chinese subtitle splitting and deterministic dynamic-inventory/medical-promise output guards.
- Bumped Gateway release version to `0.3.3`; Android code and APK versions were not changed.

## Acceptance

- Container-aligned focused regression: `58 passed`, one third-party FAISS/NumPy deprecation warning.
- Four real public dialogues passed with Doubao LLM/TTS, request IDs, approved sources where applicable, downloadable MP3 audio and no draft leakage.
- Story request dropped from repeated 60-second timeout to 8.5 seconds after deep thinking was disabled.
- Inventory request returned an explicit unable-to-confirm answer with no sources.
- Production release: `/opt/jiyangjia-ai/releases/release-task021-persona-20260812T155015Z`.
- Rollback: `/opt/jiyangjia-ai/backups/task021-persona-20260812T155015Z`.

Evidence: `docs/evidence/TASK-021/response-persona-production-20260812.md`.

## Not claimed

- No Android 12 physical-device, USB audio, Lock Task, formal signing or long-run acceptance.
- No conversational long-term memory or customer-profile storage.
- No LiveTalking, Wav2Lip, MuseTalk or GPU rendering work.
