# Current state

Updated: 2026-08-07

## TASK-014H production domain

- Canonical production domain is `ai-jiyangjia.cloud`; API base is `https://ai-jiyangjia.cloud/api/v1`; server is `120.53.86.89`.
- DNS resolves correctly through local, Cloudflare and Google resolvers.
- Server-side Nginx/TLS checks pass, Gateway is healthy/ready, `ADMIN_TOKEN` is configured, and Docker port 8080 is now loopback-only.
- The Let's Encrypt certificate is valid until 2026-11-05 and the snap renewal timer is enabled/active.
- BLOCKED: public HTTP is intercepted to the Tencent DNSPod webblock page, public HTTPS SNI is reset, and Certbot dry-run fails because its challenge is intercepted. ICP/domain access onboarding must be completed before public acceptance.
- Android production Base URL is fixed to the canonical HTTPS domain; debug builds can override with `JIYANGJIA_GATEWAY_BASE_URL` and opt into cleartext only with `JIYANGJIA_ALLOW_CLEARTEXT_GATEWAY=true`.
- Evidence: `docs/evidence/TASK-014H/production-domain-https-20260807.md`.

## TASK-015A local avatar dialogue

- PARTIAL: user-approved `E:\work\ai-kefu\资料库\人像背景.MOV` remains unchanged; ignored 1080x1920 H.264 MP4/JPG derivatives are published on the isolated local Gateway.
- The default portrait Profile binds both assets with `fit`, 36 px subtitles, 16% bottom safe area and the consult button at `(0.5, 0.9)`.
- Real browser dialogue returned a request ID, approved RAG source, Doubao answer/TTS and playable audio while the video remained decoded and looping.
- Browser recording has two completion paths: tap `结束并发送`, or detect speech and automatically stop/upload after 3 seconds of continuous silence. A 20-second maximum duration remains the fallback and no-speech startup is not auto-uploaded.
- Browser microphone capture exists but permission/recording is a manual pending check. No Android 12 physical-device result is claimed.
- Evidence: `docs/evidence/TASK-015A/local-avatar-dialogue-demo-20260807.md`.

## TASK-014C through TASK-015 update

- TASK-014C PARTIAL: secure ETag/bootstrap content synchronization, SHA-256/size/type validation, private staging, active/previous switching, offline cache and rollback are locally implemented and tested.
- TASK-014D PARTIAL: Media3 layered Display Profile renderer, fit/fill/crop geometry, normalized layout and first-frame switching are locally implemented and tested.
- TASK-014E PARTIAL: 640-byte PCM WebSocket streaming, WebRTC VAD, real Doubao partial/final stream, final-only normalization/RAG/LLM/TTS, single WAV fallback, AEC diagnostics and generation cancellation are locally implemented. Device acoustic acceptance remains open.
- TASK-014F PARTIAL: minimal DPC, BootReceiver, Home intent and guarded Lock Task are implemented; no AVD/device runtime evidence exists.
- TASK-014G PARTIAL: fail-closed controlled signing, release manifest and verified PackageInstaller path are implemented. Disposable test signing passed and artifacts were deleted; formal identity/hosting/device upgrade are absent.
- TASK-015 BLOCKED / NO-GO: no Android device or AVD, trusted HTTPS release host or formal signing custody/N-series APKs. Approved portrait media/Profile now exists locally but is not yet production-hosted. Gateway tests: 63 passed. Android unit/lint/debug assembly and repository verification pass.

## Completed

- `main` 分支已对齐到远端提交 `a68f234`，`TASK-014A` 已入库为正式主线内容，不再作为本地待完成开发项。
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
- TASK-009 Doubao TTS adapter is complete for provider acceptance:
  - real Doubao/Volcengine V3 unidirectional HTTP streaming adapter exists;
  - legacy V1 HTTP compatibility remains;
  - CLI helper and unit tests exist;
  - Mock TTS returns deterministic audio bytes;
  - real Doubao TTS call using private external env generated verified MP3 evidence.
- TASK-010 Doubao ASR adapter is complete for provider acceptance:
  - real Doubao/Volcengine big-model WebSocket adapter exists;
  - Gateway uses bounded file/bytes-to-WebSocket chunks, not Android always-on streaming;
  - non-WAV/PCM input is normalized to 16 kHz mono PCM WAV before ASR;
  - CLI helper and tests exist;
  - real Doubao ASR call using private external env generated verified transcript evidence.
- TASK-011 LLM/Embedding adapters are complete:
  - OpenAI-compatible Chat provider exists for DeepSeek, Doubao/Volcengine Ark and generic compatible endpoints;
  - OpenAI-compatible Embedding provider exists for Doubao/Ark and generic compatible endpoints;
  - Doubao/Ark Embedding supports both `/embeddings` and `/embeddings/multimodal` routes;
  - CLI helpers and `tests/llm` exist;
  - real DeepSeek LLM and real Doubao/Ark LLM calls succeeded using private external env;
  - real Doubao/Ark Embedding call succeeded with `doubao-embedding-vision-251215`, returning 2048-dimensional vectors.
- TASK-012 lightweight RAG is complete for local/backend acceptance:
  - SQLite stores document/chunk metadata and ingestion runs;
  - SQLite FTS5 provides keyword retrieval;
  - FAISS provides Top-K vector retrieval through the EmbeddingProvider;
  - explicit JSON/YAML/Markdown/TXT/PDF/DOCX parsing is supported;
  - customer search defaults to `approved` only while `draft` requires an explicit internal flag and `rejected` is excluded;
  - prohibited medical/price/promotion/inventory/member-balance/internal queries return safe transfer text;
  - source citations and `request_id` are returned by knowledge search and dialogue flows;
  - real Doubao/Ark embedding-backed evaluation passed with 2048-dimensional vectors.
- TASK-013 is partial-complete:
  - Android records PCM, wraps it as WAV and uploads it to Gateway `/api/v1/dialogue/audio`;
  - Android downloads generated `/api/v1/audio/{audio_id}` bytes and plays encoded answer audio through `MediaPlayer`;
  - Android displays transcript, answer subtitle, request ID and source diagnostics;
  - Android cancel/service-error paths return to idle-video/fallback state;
  - backend Mock E2E and 30-cycle stability tests passed;
  - one real private-env Gateway smoke passed through Doubao ASR, Doubao/Ark Embedding RAG, Doubao/Ark LLM and Doubao TTS;
  - Gateway normalizes common ASR homophones of `积养家` before RAG/LLM and preserves provider output as `transcript.raw_text` when changed;
  - Android real-device install/record/playback/subtitle behavior remains unverified.
- TASK-014 is DONE:
  - Tencent Cloud host `120.53.86.89` runs the force-recreated Gateway image with FFmpeg `7.1.5-0+deb13u1`.
  - `/opt/jiyangjia-ai/secrets/.env.local` has mode `600`; ASR/TTS/LLM/Embedding all report ready.
  - One final acceptance passed for text, Android-format WAV and MP3 through ASR -> RAG -> LLM -> TTS -> audio fetch.
  - WAV and MP3 both returned `request_id`, non-empty `sources`, `audio_id` and downloadable `audio/mpeg`.
  - Eight conflicting TASK-014 test documents were downgraded to draft; approved knowledge now contains the 10 controlled TASK-012 FAQ entries.
- TASK-014 now includes hardened diagnostics:
  - `/api/v1/readiness`；
  - 统一 provider 配置检查；
  - `/api/v1/dialogue/*` 已提供 `failed_stage` 信息用于错误分层（用于后续回归，不影响本次通过）。

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
- `scripts\test_tts_provider.py --provider doubao --check-config`: returns only missing/configured status.
- `.env.example` is aligned to TASK-009 TTS variable names and contains placeholders only.
- `python -m pytest tests\tts tests\gateway -q`: 10 passed after V3 update.
- `scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config`: returned `ok=true` with configured app/access auth, speaker and resource ID; values were not printed.
- `scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3`: generated `audio/mpeg`, `20589` bytes, SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`.
- `ffprobe tmp\doubao-tts-test.mp3`: MP3, 24000 Hz, mono, 2.568 seconds.
- `python -m pytest tests\asr tests\gateway tests\tts -q`: 16 passed after ASR implementation.
- `scripts\test_asr_provider.py --provider mock --file tmp\doubao-tts-test.mp3 --content-type audio/mpeg`: returned deterministic mock transcript.
- `scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config`: returned `ok=true`; values were not printed.
- `scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --file tmp\doubao-tts-test.mp3 --content-type audio/mpeg`: generated real ASR transcript `您好，欢迎来到机养家。` after MP3-to-WAV normalization.
- `ffprobe tmp\doubao-tts-test-16k.wav`: WAV, PCM s16le, 16000 Hz, mono, 2.568 seconds.
- `python -m pytest tests\llm tests\gateway tests\asr tests\tts -q`: 25 passed after TASK-011.
- `scripts\test_llm_provider.py --provider deepseek --env-file E:\work\ai-kefu\.env.local --prompt ...`: real LLM call succeeded; usage metadata present.
- `scripts\test_llm_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --prompt ...`: real LLM call succeeded; usage metadata present.
- `scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config`: configuration preflight passed with the default verified embedding model.
- `scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "积养家门店服务时间"`: real provider returned 1 vector, 2048 dimensions, usage metadata present.
- `python -m pytest tests\llm tests\gateway tests\asr tests\tts -q`: 27 passed after multimodal Embedding support.
- `python -m pytest tests\knowledge -q`: 6 passed after TASK-012 RAG implementation.
- `python -m pytest tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q`: 34 passed after TASK-012.
- `scripts\evaluate_lightweight_rag.py --data knowledge-test`: Mock RAG evaluation passed 24/24 cases.
- `scripts\evaluate_lightweight_rag.py --data knowledge-test --provider doubao --env-file E:\work\ai-kefu\.env.local`: real Doubao/Ark Embedding RAG evaluation passed 24/24 cases with 2048-dimensional vectors; values were not printed.
- Gateway API smoke passed for real embedding-backed `/api/v1/knowledge/index`, `/api/v1/knowledge/search` and `/api/v1/knowledge/status`.
- `python -m pytest tests\e2e -q`: 3 passed after TASK-013.
- `python -m pytest tests\e2e tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q`: 37 passed after TASK-013.
- TASK-013 Mock 30-cycle Gateway dialogue report: 30 passed, 0 failed, 0 fallback, average local TestClient latency 4.33 ms.
- TASK-013 real Provider Gateway smoke: Doubao ASR + Doubao/Ark Embedding + Doubao/Ark LLM + Doubao TTS succeeded; output audio was `audio/mpeg`, `69741` bytes.
- Android `testDebugUnitTest`, `assembleDebug` and `lintDebug` passed with project-local JDK 17.
- TASK-013 debug APK: `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `862144`, SHA-256 `263B1FA8E8DB2198E93B4E4FFC85E715CEE2556E0511C67B002D7E588C76BC8E`.
- TASK-013 brand normalization: `机养家`, `季养家`, `寄养家`, `吉阳家`, `积阳家` and `济氧家` normalize to `积养家`; `python -m pytest tests\asr tests\gateway tests\e2e -q` passed with 19 tests and full backend regression passed with 42 tests.
- TASK-014 evidence reconciliation: imported and re-verified on 2026-08-07 with real provider/env readiness.
- TASK-014 final acceptance: `docs/evidence/TASK-014/task014-final-acceptance-20260807.json` -> text/WAV/MP3 and all summary gates passed.
- TASK-014 operational evidence: `task014-gateway-build-final-20260807.txt`, `task014-provider-env-final-20260807.json`, `task014-knowledge-cleanup-final-20260807.json`.
- TASK-014A full regression after browser repair: `python -m pytest tests -q` -> 55 passed; failed embedding publication returns to draft, uploaded assets require real file signatures, and Display Profiles only bind published assets.
- TASK-014A management JavaScript: generated page script passed `node --check`.
- TASK-014A local HTTP: four admin pages, system status, manifest and 1920x1080 profile matching returned HTTP 200 with request IDs.
- TASK-014A valid-file HTTP: generated H.264 MP4 was uploaded, downloaded through authenticated preview and verified by ffprobe at 640x360; PNG and Markdown publish flows returned manifest/source/request IDs.
- TASK-014A browser audit found the first UI acceptance gap: action commands used two-part strings while the dispatcher expected three parts, so preview/approve/publish buttons reloaded data without issuing POST requests. Status returned to IN_PROGRESS pending browser-level repair and re-verification.
- TASK-014A browser repair completed: command dispatch now uses `scope-action:id`; knowledge, asset, display and system buttons were clicked in the real in-app browser and backend state changes were observed with no application console errors. Evidence: `task014a-real-browser-actions-20260807.json`.
- TASK-014A workflow tests cover PDF/DOCX/MD/TXT parsing, draft exclusion, explicit publish, sources, MP4/JPG/PNG metadata, protected draft preview, publish/rollback, SHA-256, four presets, custom profile matching and SQLite persistence after store recreation.

## Not completed

- OpenAI-compatible fallback LLM with a non-DeepSeek, non-Doubao third provider.
- Formal production knowledge base beyond the scoped demo FAQ set.
- Android 12 large-screen real-device acceptance.
- TASK-014A production deployment and production `ADMIN_TOKEN` configuration.
- Production publication of the approved local portrait media/Profile, formal business knowledge and device-measured Profile tuning.
- Android 12 physical validation of secure sync, Display Profile, USB/AEC, managed kiosk, signed update/rollback and long-run operation.

## Next action

Complete the local browser microphone permission check, then resume `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md` only after all remaining external gates in `memory/PENDING_INPUTS.md` are available. Do not claim production deployment or device acceptance.
