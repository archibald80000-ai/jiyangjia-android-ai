# Handoff

Updated: 2026-08-07

## Current project position

- Project: `jiyangjia-android-ai`
- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`
- Current task status: `TASK-014 DONE`
- Next task: `TASK-014A_ADMIN_CONTENT_DISPLAY.md` (`PLANNED`)
- Raw business materials: `E:\work\积养家` (read-only; do not scan or bulk import)
- Phase 1 remains the Android 12 idle-video voice RAG MVP. LiveTalking/Wav2Lip/MuseTalk/WebRTC/GPU inference remain deferred.

## Verified implementation

- TASK-008 Gateway skeleton: DONE.
- TASK-009 real Doubao TTS: DONE.
- TASK-010 real Doubao ASR: DONE.
- TASK-011 real LLM and Embedding adapters: DONE.
- TASK-012 lightweight RAG: DONE. SQLite, FTS5, FAISS, reviewed statuses, PDF/DOCX/MD/TXT parsing and source citations are implemented.
- TASK-013: PARTIAL only because Android 12 physical-device acceptance is pending. Android code records PCM, wraps WAV, uploads to Gateway, displays transcript/answer/sources, fetches TTS audio and plays it before returning to idle.

## TASK-014 final production state

- Tencent Cloud host: `120.53.86.89`, Ubuntu 24.04, CPU-only.
- Gateway container is `running/healthy` after a gateway-only image build and forced recreate.
- Production Compose loads `/opt/jiyangjia-ai/secrets/.env.local`; the file exists with mode `600`.
- `scripts/check_provider_env.py --require-real-mvp` reports real Doubao ASR/TTS/LLM/Embedding ready without printing values.
- Online image contains FFmpeg `7.1.5-0+deb13u1`.
- Final acceptance passed for text, Android-format WAV (`16 kHz`, mono, PCM 16-bit) and MP3 uploads.
- WAV and MP3 both completed ASR -> RAG -> LLM -> TTS, returned `request_id`, non-empty `sources`, `audio_id`, and downloadable `audio/mpeg`.
- Eight conflicting TASK-014 test records were downgraded from `approved` to `draft`. The production-facing approved set is now the 10 controlled TASK-012 FAQ entries.
- Knowledge rollback backup: `/opt/jiyangjia-ai/backups/task014-knowledge-cleanup-20260807-125648`.

## Final evidence

- `docs/evidence/TASK-014/task014-final-acceptance-20260807.json`
- `docs/evidence/TASK-014/task014-gateway-build-final-20260807.txt`
- `docs/evidence/TASK-014/task014-provider-env-final-20260807.json`
- `docs/evidence/TASK-014/task014-knowledge-cleanup-final-20260807.json`
- `docs/evidence/TASK-014/TASK-014_FINAL_ACCEPTANCE.md`

## Human inputs still required

- Reviewed formal business knowledge beyond the controlled demo FAQ set.
- First approved idle-character MP4/background and rights confirmation.
- Target Android screen resolution, density, orientation, safe area and audio hardware details.
- Android 12 physical device for TASK-015 USB microphone, speaker, network, reboot and long-run acceptance.

## Next action

Execute exactly one next task: `TASK-014A_ADMIN_CONTENT_DISPLAY.md`. Implement the lightweight admin/content/display skeleton locally and verify persistence/API contracts before TASK-015.

## Safety boundaries

- No Dify, LangFlow or Flowise.
- No bulk scan/upload of `E:\work\积养家`.
- No secrets, APKs, raw recordings, model weights, production DB/FAISS or business source files in Git.
- New knowledge defaults to `draft`; only reviewed `approved` content may serve customers.
