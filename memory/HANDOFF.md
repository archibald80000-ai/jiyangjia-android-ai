# Handoff

Updated: 2026-08-06

## Current project position

- Project: `jiyangjia-android-ai`
- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`
- Raw business materials: `E:\work\积养家` — read-only by default; do not scan or bulk import.
- Phase 1 product route: Android 12 idle-character-video voice RAG MVP. LiveTalking/Wav2Lip/MuseTalk/WebRTC/GPU inference remain deferred.

## Verified implementation

- TASK-008 Gateway skeleton: DONE.
- TASK-009 real Doubao TTS: DONE.
- TASK-010 real Doubao ASR: DONE.
- TASK-011 real LLM + Embedding adapters: DONE.
- TASK-012 lightweight RAG: DONE — SQLite metadata, FTS5, FAISS, reviewed statuses, PDF/DOCX/MD/TXT parsing, source citations.
- TASK-013: PARTIAL only because Android 12 physical-device acceptance is pending. Android code already records PCM, wraps WAV, uploads to Gateway, displays transcript/answer/source diagnostics, fetches TTS audio and plays it before returning to idle.
- Backend real-provider smoke has succeeded locally through ASR -> RAG/Embedding -> LLM -> TTS -> audio fetch.

## Current blocker — TASK-014

Tencent Cloud current Gateway code is deployed and health/config/knowledge endpoints are reachable. Real dialogue is still blocked by the server Provider environment chain:

- `/api/v1/dialogue/text` -> `503 BLOCKED_PROVIDER_CREDENTIALS`
- `/api/v1/dialogue/audio` -> `503 BLOCKED_PROVIDER_CREDENTIALS`

This is not an upload transport failure. Required remediation:

1. verify `/opt/jiyangjia-ai/secrets/.env.local` exists with mode 600;
2. verify production Compose actually loads that fixed secret file;
3. run `scripts/check_provider_env.py --require-real-mvp` and report only configured/missing;
4. recreate the Gateway container so new env is loaded;
5. verify `/api/v1/readiness`;
6. run one dialogue/text + audio fetch and one dialogue/audio + audio fetch acceptance.

Do not print or commit secret values.

## New planned task — TASK-014A

A new task specification is added at:

`tasks/TASK-014A_ADMIN_CONTENT_DISPLAY.md`

Purpose: add a very lightweight browser admin layer for non-developers.

Scope:

- knowledge upload/review/chunk preview/reindex/search test;
- reuse TASK-012 SQLite/FTS5/FAISS/Embedding rather than rebuilding RAG;
- MP4 idle-character video and JPG/PNG background asset management;
- publish/rollback + asset manifest;
- Display Profiles for 1920x1080, 3840x2160, 1280x720, 1080x1920 and custom sizes;
- Android should select/cache the matching display profile and asset version without requiring a new APK for each screen size;
- `/api/v1/admin/*` protected by a server-side `ADMIN_TOKEN` for Phase 1.

TASK-014A should be developed locally first. It must not claim server or Android physical-device acceptance until those are actually tested.

## Human inputs still required

Canonical checklist:

`memory/PENDING_INPUTS.md`

Key missing inputs:

- production Provider secret configuration on Tencent Cloud;
- reviewed formal business knowledge beyond demo FAQ;
- first approved digital-human idle MP4/background and rights confirmation;
- target Android screen's actual resolution/density/orientation/audio hardware information;
- Android 12 physical device for TASK-015.

## Recommended execution order

1. Finish TASK-014 Provider env-chain remediation and server real-provider acceptance.
2. Implement TASK-014A lightweight admin/content/display management locally and test persistence/API contracts.
3. Prepare one approved idle-video asset and one small reviewed knowledge set through the admin flow.
4. Execute TASK-015 on the real Android 12 large screen: install, resolution/profile, USB mic, speaker, network recovery, reboot and long-run tests.
5. Only after Phase 1 acceptance revisit LiveTalking real-time lip-sync work.

## Safety boundaries

- No Dify/LangFlow/Flowise.
- No bulk scan/upload of `E:\work\积养家`.
- No secrets, APKs, raw recordings, model weights, production DB/FAISS or business source files in Git.
- New knowledge defaults to `draft`; only reviewed `approved` content may serve customers.
