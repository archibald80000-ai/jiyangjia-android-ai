# Handoff

Updated: 2026-08-07

## Current project position

- Project: `jiyangjia-android-ai`
- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`
- Current branch: `task/TASK-020B-avatar-knowledge-binding`, stacked on completed TASK-020A commit `dd1307c`.
- Current task status: `TASK-020B DONE locally`; `TASK-014H BLOCKED_BY_TENCENT_WEBBLOCK_ICP`; `TASK-015 BLOCKED / NO-GO`.
- Next action: after TASK-014H clears, publish the accepted knowledge/assets/Profile to production and run one bounded production acceptance.
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

Complete ICP/domain access onboarding for TASK-014H, then publish the accepted knowledge/assets/Profile to production and verify it once. Do not claim or repeat TASK-015 acceptance while public HTTPS and physical-device gates remain blocked.

## Safety boundaries

- No Dify, LangFlow or Flowise.
- No bulk scan/upload of `E:\work\积养家`.
- No secrets, APKs, raw recordings, model weights, production DB/FAISS or business source files in Git.
- New knowledge defaults to `draft`; only reviewed `approved` content may serve customers.
