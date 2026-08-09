# Handoff

Updated: 2026-08-09

## Current project position

- Project: `jiyangjia-android-ai`
- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`
- Current branch: `task/TASK-020F-aiye-product-knowledge-v22`.
- Current task status: `TASK-020F DONE / PRODUCTION_PUBLISHED`; `TASK-020C PARTIAL (production published, public HTTPS blocked)`; `TASK-014H BLOCKED_BY_TENCENT_WEBBLOCK_ICP`; `TASK-015 BLOCKED / NO-GO`.
- Next action: clear TASK-014H, then externally verify the already-published demo and read-only status links once.
- Raw business materials: `E:\work\积养家` (read-only; do not scan or bulk import)
- Phase 1 remains the Android 12 idle-video voice RAG MVP. LiveTalking/Wav2Lip/MuseTalk/WebRTC/GPU inference remain deferred.

## Verified implementation

- TASK-008 Gateway skeleton: DONE.
- TASK-009 real Doubao TTS: DONE.
- TASK-010 real Doubao ASR: DONE.
- TASK-011 real LLM and Embedding adapters: DONE.
- TASK-012 lightweight RAG: DONE. SQLite, FTS5, FAISS, reviewed statuses, PDF/DOCX/MD/TXT parsing and source citations are implemented.
- TASK-013: PARTIAL only because Android 12 physical-device acceptance is pending. Android code records PCM, wraps WAV, uploads to Gateway, displays transcript/answer/sources, fetches TTS audio and plays it before returning to idle.
- TASK-014A: DONE locally. FastAPI management pages, explicit knowledge publication, media version/rollback/manifest, editable Display Profiles and persistence are covered by 55 tests and real-browser button verification.
- TASK-014C: PARTIAL; secure versioned content sync and rollback pass local tests.
- TASK-014D: PARTIAL; Media3 Display Profile renderer passes local geometry/build/lint tests.
- TASK-014E: PARTIAL; WebRTC VAD and real Doubao bidirectional partial/final streaming pass, while physical AEC/barge-in remains pending.
- TASK-014F: PARTIAL; DPC/boot/Home/Lock Task code builds, but no Device Owner runtime exists.
- TASK-014G: PARTIAL; controlled signing/update validation passes with a deleted disposable test identity, but formal signing and device upgrades are absent.
- TASK-015A: PARTIAL; approved portrait media/Profile and a real local browser RAG/LLM/TTS dialogue pass. Manual end/send plus speech-first 3-second silence auto-send are implemented. Browser microphone permission is not yet manually accepted and no Android device result exists.
- TASK-014H: BLOCKED externally. Canonical domain configuration, internal TLS/Nginx/Gateway, loopback-only 8080 and Android URL are complete; Tencent DNSPod webblock prevents public HTTP/HTTPS and ACME renewal validation.
- TASK-020A: DONE locally. Real Doubao Embedding imported 65 reviewed documents on isolated port 8090; final state is 41 approved, 24 draft, 65 chunks and 65 vectors at 2048 dimensions. Current-policy 80-case acceptance is 100%, sources completeness is 100% and draft leaks are 0. The preserved port-18081 demo database was not switched.
- TASK-020B: DONE locally. The TASK-020A candidate is bound to the isolated port-18084 avatar demo with real ASR/TTS/LLM/Embedding; API WAV and browser text dialogues passed with approved sources, playable TTS and the 1080x1920 presentation intact.
- TASK-020C: PARTIAL. Production now uses the formal 41/24 knowledge state and the approved MOV-derived 1080x1920 avatar/background bound to the default Profile. Real dialogue and server-local TLS pass; external HTTPS remains blocked.
- TASK-020D: DONE. The explicitly authorized v2.1 JSON is tracked under `knowledge-public/v2.1/`; production was backed up and re-imported in 50+15 batches with real Doubao Embedding. Final 80-case current-policy acceptance is 100%, sources are complete and draft leaks are 0.
- TASK-020E: DONE / READY_FOR_DEMO. Isolated port 8091 uses real Doubao ASR/TTS/LLM/Embedding with a new 41/24/65 candidate. Search passed 80/80 and five synthetic-speech audio dialogue scenarios passed after scoped short-query and `七膳` homophone adaptations. This is not human microphone or Android device evidence.
- TASK-020F: DONE / PRODUCTION_PUBLISHED. The public v2.2 package contains 204 documents (180 approved, 24 draft), including 139 new source-traced Aiye records. Local and production Top-3 retrieval passed 240/240 with 340 x 2048 real Doubao vectors, sources 100% and draft leaks 0. Six text plus one synthetic-speech audio dialogue passed the real production chain. Public HTTPS remains a separate TASK-014H blocker.

## TASK-020F package and production rollback

- Employee/public package: `knowledge-public/v2.2/README.md`.
- Source archive: `knowledge-public/v2.2/sources/aiye-foods/` (25 HTML files with hashes in `manifest.json`).
- Import order: `import_batch_01.json` through `import_batch_05.json`; do not submit `import_all.json` to the Gateway.
- Production SQLite/FAISS: `/opt/jiyangjia-ai/current/var/knowledge/jiyangjia.db` and `faiss.index`.
- Production rollback: `/opt/jiyangjia-ai/backups/task020f-20260809T035803Z`.
- Evidence: `docs/evidence/TASK-020F/aiye-knowledge-v22-acceptance-20260809.md`.

## TASK-020E runtime and rollback

- Gateway: `http://127.0.0.1:8091` while PID from `var/task020e/20260808T055957Z/candidate/gateway.pid` remains running.
- Candidate SQLite/FAISS: `var/task020e/20260808T055957Z/candidate/knowledge.db` and `faiss.index`.
- Preserved demo/real backups: `var/task020e/20260808T055957Z/backups/pre-import/`.
- Raw ignored evidence: `var/task020e/20260808T055957Z/candidate/`.
- Evidence: `docs/evidence/TASK-020E/gateway-real-import-acceptance-20260808.md`.

## TASK-020D public package and rollback

- Public employee entry: `knowledge-public/README.md`.
- Full review file: `knowledge-public/v2.1/import_all.json`.
- Gateway import files: `knowledge-public/v2.1/import_batch_01.json`, then `import_batch_02.json`; the API rejects more than 50 documents per request.
- Manifest/checksums: `knowledge-public/v2.1/manifest.json`.
- Production rollback backup: `/opt/jiyangjia-ai/backups/task020d-public-knowledge-20260808T034524Z`.
- Evidence: `docs/evidence/TASK-020D/public-knowledge-package-import-20260807.md`.

## TASK-020C production paths

- SQLite: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/jiyangjia.db`
- FAISS: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/faiss.index`
- Assets: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/assets/`
- Backup: `/opt/jiyangjia-ai/backups/task020c-avatar-20260808T031244Z`
- Target demo: `https://ai-jiyangjia.cloud/demo/kiosk` after TASK-014H unblock.
- Evidence: `docs/evidence/TASK-020C/production-knowledge-avatar-sharing-20260807.md`.

## TASK-020B runtime and rollback

- Demo URL: `http://127.0.0.1:18084/demo/kiosk` while the isolated process remains running.
- Bound SQLite/FAISS: `var/task014a-dev/task020a-candidate-20260808T023610Z/`.
- Rollback backup: `var/local-avatar-demo/backups/task020b-20260808T025409Z/`.
- Runtime dialogue evidence remains ignored at `var/local-avatar-demo/task020b-20260808T025409Z/`.
- Public source URIs are sanitized to `knowledge://<doc_id>`; original local source paths are not returned.
- Evidence: `docs/evidence/TASK-020B/avatar-knowledge-binding-20260807.md`.

## TASK-020A runtime and rollback

- Existing active files: `var/task014a-dev/knowledge.db` and `var/task014a-dev/faiss.index`.
- Required backups: `knowledge.db.backup.20260808T023610Z` and `faiss.index.backup.20260808T023610Z` in the same ignored directory.
- Candidate: `var/task014a-dev/task020a-candidate-20260808T023610Z/`.
- Candidate Gateway: `http://127.0.0.1:8090`; it uses real Doubao Embedding and must not be confused with the Mock-Embedding port-18081 demo.
- ASR, TTS and LLM on 8090 are Mock. The next dialogue task must use real providers before claiming an AI avatar voice demonstration.
- Raw 80-case output stays in ignored runtime state and must not be committed or uploaded.
- Evidence: `docs/evidence/TASK-020A/formal-knowledge-import-acceptance-20260807.md`.

## TASK-014H server state

- Canonical URL: `https://ai-jiyangjia.cloud`; API: `https://ai-jiyangjia.cloud/api/v1`; admin target: `https://ai-jiyangjia.cloud/admin`.
- Active release Compose: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/deploy/docker-compose.yml`.
- Rollback backup: `/opt/jiyangjia-ai/backups/task014h-domain-20260807T103746Z`.
- Gateway container is healthy and bound to `127.0.0.1:8080`; Nginx listens on 80/443; UFW allows only 22/80/443.
- Certificate exists and is valid until 2026-11-05; snap Certbot timer is active, but dry-run currently fails at the Tencent webblock interception.
- Do not retry Nginx/Certbot changes until the ICP/access block is released; then run the commands in `docs/server/operations.md` once.

## TASK-015A local demo

- URL: `http://127.0.0.1:18084/demo/kiosk` while the isolated development process remains running.
- Runtime state: ignored `var/local-avatar-demo/`; provider values are loaded from the external private env and are never printed or committed.
- Media: 1080x1920 H.264 silent MP4 plus same-source JPG, published and bound to `display-1080x1920`.
- Real browser result: video decoded at 1080x1920, remained playing during dialogue, and displayed request ID, approved source, subtitle and TTS playback with no subtitle/button or source/button overlap.
- Recording behavior: the button remains `结束并发送`; after confirmed speech, three continuous silent seconds automatically stop and upload the same recording. Without detected speech it waits for manual stop or the 20-second maximum-duration fallback.
- Remaining local check: click `开始咨询`, grant microphone permission and speak one question.

## TASK-014A local state

- Branch: `main`（`task/TASK-014A-admin-content-display` 已完成并入 `main`）。
- Local admin: `http://127.0.0.1:18081/admin/system` while the development process remains running.
- Runtime state is under ignored `var/task014a-dev/`.
- Production admin API requires `ADMIN_TOKEN`; no value is stored in Git or page source.
- Evidence: `docs/evidence/TASK-014A/`.
- Browser acceptance: `task014a-real-browser-actions-20260807.json`; do not regress to HTTP-200-only UI acceptance.
- Not completed: Tencent deployment, formal content/media import, Android manifest/profile consumption and physical-device validation.

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

- No additional formal knowledge content is required for the v2.1 demo gate; future content changes still require review and versioned approval.
- Target Android screen resolution, density, orientation, safe area and audio hardware details.
- Android 12 physical device for TASK-015 USB microphone, speaker, network, reboot and long-run acceptance.

## Next action

Complete ICP/domain access onboarding for TASK-014H, then externally verify the already-published v2.2 demo/status/manifest/Profile once. Do not claim or repeat TASK-015 acceptance while public HTTPS and physical-device gates remain blocked.

## Safety boundaries

- No Dify, LangFlow or Flowise.
- No bulk scan/upload of `E:\work\积养家`.
- No secrets, APKs, raw recordings, model weights, production DB/FAISS or business source files in Git.
- New knowledge defaults to `draft`; only reviewed `approved` content may serve customers.
