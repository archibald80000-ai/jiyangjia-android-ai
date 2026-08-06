# Current state

Updated: 2026-08-06

## Completed

- Product scope and development order documented.
- LiveTalking upstream identified and commit lock recorded, but LiveTalking/Wav2Lip/MuseTalk/WebRTC/GPU inference are deferred.
- TASK-000 environment/repository audit completed.
- TASK-001 upstream audit completed.
- TASK-002 isolated LiveTalking runtime completed historically; not a Phase 1 blocker.
- TASK-003/TASK-004/TASK-006/TASK-016 are deferred for the future LiveTalking enhancement phase.
- TASK-005 Android kiosk shell is locally built/tested; real Android 12 install/rendering remains unverified.
- TASK-007 Android audio source is partial-complete: runtime mic permission, diagnostics, USB-first route policy, recording/playback and source-side device change monitoring are implemented. Real USB mic/speaker validation is deferred to TASK-015.
- TASK-008 FastAPI Gateway and unified Provider skeleton are complete locally:
  - required health/dialogue/knowledge/audio/config endpoints;
  - Mock ASR/TTS/LLM/Embedding providers;
  - SQLite knowledge skeleton with `approved`, `draft`, `rejected`;
  - request IDs, sources and generated `audio_id`;
  - tests and local HTTP verification passed.
- TASK-009 Doubao TTS adapter is partial-complete:
  - real Doubao/Volcengine HTTP TTS adapter code exists;
  - CLI helper and unit tests exist;
  - Mock TTS returns deterministic audio bytes;
  - real Doubao TTS call is blocked by missing credentials.

## Route changed

- Phase 1 goal is now Android large-screen voice RAG MVP:

```text
Android recording
-> Doubao ASR
-> lightweight RAG
-> Doubao/Volcengine Ark or OpenAI-compatible LLM
-> Doubao TTS
-> Android playback/subtitles
-> idle video
```

- No Dify, LangFlow or Flowise.
- Knowledge route: selected reviewed Markdown/TXT/PDF/DOCX -> SQLite -> EmbeddingProvider -> local FAISS -> Top-K with sources.
- Android real-device acceptance is delayed to TASK-015 and does not block local provider/RAG development.

## Verified this task

- Python 3.10 local venv: `.venv\gateway-task008-py310`.
- `python -m pytest tests\gateway -q`: 4 passed.
- `python -m gateway --help`: exit 0.
- Local HTTP checks on `127.0.0.1:18080` passed for health, client config, knowledge index/search, text dialogue and audio fetch.
- Port `8080` was occupied locally; this is logged as a local issue.
- `python -m pytest tests\tts tests\gateway -q`: 8 passed after adding Gateway `doubao` missing-credential regression coverage.
- `python -m pytest tests\tts tests\gateway -q`: 9 passed after adding TTS config preflight redaction coverage.
- `scripts\test_tts_provider.py --provider mock`: returned deterministic audio bytes.
- `scripts\test_tts_provider.py --provider doubao`: returned `BLOCKED_PROVIDER_CREDENTIALS` because `DOUBAO_TTS_APP_ID`, `DOUBAO_TTS_ACCESS_TOKEN` and `DOUBAO_TTS_VOICE_TYPE` are missing.
- `scripts\test_tts_provider.py --provider doubao --check-config`: returns only missing/configured status.
- `.env.example` is aligned to TASK-009 TTS variable names and contains placeholders only.

## Not completed

- Real Doubao TTS API call with credentials.
- Real Doubao ASR.
- Real Doubao/Volcengine Ark LLM.
- OpenAI-compatible fallback LLM.
- Real Embedding API.
- FAISS production index and document parsing.
- Android end-to-end integration with Gateway.
- Tencent Cloud deployment for the new provider/RAG route.
- Android 12 large-screen real-device acceptance.

## Next action

Continue exactly one next action for `TASK-009_TTS_PROVIDERS.md`: configure `DOUBAO_TTS_APP_ID`, `DOUBAO_TTS_ACCESS_TOKEN` and `DOUBAO_TTS_VOICE_TYPE` in `.env.local` or server environment, then rerun the real Doubao TTS CLI test.
