# TASK-017 formal knowledge activation — 2026-08-07

## Result

`DONE / FORMAL GATEWAY SWITCHED`.

The owner explicitly authorized the formal switch after the brand-prefix retrieval defect was fixed. The Tencent Cloud Gateway now serves the v2.1 curated knowledge set with scoped business/general answer routing.

## Local fix and gate

- Commit: `f6d24f4 fix(knowledge): normalize brand-prefixed boundary queries [TASK-017]`.
- The brand name selects the business corpus but is removed from lexical scoring inside that corpus.
- Strong keyword-only evidence requires at least `0.7`; low-confidence unknown-product matches remain rejected.
- Membership tests added for both `积养家会员余额怎么查询` and `帮我查一下积养家会员余额`, plus branded generic price.
- TASK-017 regression: `50 passed, 1 unrelated TASK-015A test deselected`.
- Full repository excluding the same unrelated Kiosk assertion: `87 passed, 1 deselected`.
- Real 8090 retrieval remained: approved target top-1 `36/36`, draft exclusion `14/14`, general bypass `6/6`, draft leaks `0`.

## Formal target and pre-switch state

- Host: `120.53.86.89`, SSH user `ubuntu` with public-key authentication.
- Active container: `jiyangjia-gateway`.
- The initial active release was TASK-015A, then a concurrent TASK-015B realtime deployment replaced the container during the switch window.
- TASK-017 routing first landed on `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T094900Z`. A later concurrent TASK-015B rollout preserved the same verified routing hashes and shared knowledge data; the final observed active release is `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z`.
- The TASK-015B `main.py`, Kiosk, assets and admin database were preserved. Only `answer_policy.py`, `knowledge.py`, `llm.py`, `providers.py` and `schemas.py` were installed.
- Previous formal knowledge: 11 approved, 9 draft, 1 rejected; SQLite integrity `ok`.
- Previous SQLite SHA-256: `8A59DE54DDB604871DB973655436405D2F147C53FBD3B8086146D5FBB95B3B73`.
- Previous FAISS SHA-256: `4EC52836505F8EBF0507B023BB6569C90A645F2BAB3C459BC354C5B40E42BD25`.

## Backups and rollback

Independent backups were created before mutation:

- Previous formal data and code: `/opt/jiyangjia-ai/backups/task017-before-task017-20260807T094735Z`.
- TASK-015B pre-routing code plus candidate data: `/opt/jiyangjia-ai/backups/task017-before-code-task015b-task017-20260807T094735Z`.
- Both backup SQLite files passed `PRAGMA integrity_check`; `SHA256SUMS` manifests are stored in both directories.

All release `var/knowledge` paths resolve to the shared `/opt/jiyangjia-ai/var/knowledge`. A release-local copy is therefore not an independent rollback. Full rollback must stop the current TASK-015B compose service, restore code from the TASK-015B code backup, remove `answer_policy.py`, restore the old SQLite/FAISS through temporary files plus atomic `mv` into the shared directory, recreate the Gateway, then verify health/readiness and hashes.

## Activated knowledge

- Documents: 65 total, 41 approved, 24 draft, 0 rejected.
- Chunks/embeddings/vectors: 65/65/65.
- Vector dimensions: 2048; Embedding provider ready.
- SQLite integrity: `ok`.
- SQLite SHA-256: `E8C744E4D2887A74D37CB23768390D449BE582B51D131ECA03D09D11EA834BCE`.
- FAISS SHA-256: `BE2E0969248B1020C04B6C6862C6A3CE0C5C50FAED1115657489516A70995B6C`.
- Public `include_draft=true`: HTTP 422.
- Task-created `/tmp/task017-20260807T094735Z` staging directory was removed after verification.

## Formal HTTPS and real-provider acceptance

Windows system Schannel validated `https://120.53.86.89` without disabling TLS checks. Health and readiness were HTTP 200; ASR, TTS, LLM and Embedding all reported ready.

| Case | Knowledge/result | Answer source |
|---|---|---|
| Member balance with brand prefix | `faq_boundary_006`, approved | `knowledge_grounded` |
| Generic price with brand prefix | `faq_boundary_002`, approved | `knowledge_grounded` |
| Specific draft maintenance price | no match | `in_domain_unverified` |
| Internal password | no match | `in_domain_unverified` |
| Unknown durian product | no match | `in_domain_unverified` |
| General arithmetic | no match | `general_answer` |

Real Doubao TTS returned downloadable `audio/mpeg` for six checked audio IDs, all HTTP 200. One LLM response returned `LLM_NO_TEXT`; it was retried once, succeeded, and was not repeatedly probed.

The server sends a currently valid Let's Encrypt `YE2/Root YE` chain. The local Python 3.10 CA bundle rejected that new chain while Windows Schannel validated it; Android 12 certificate trust must still be confirmed on the physical device and is not claimed by TASK-017.

## Deployment incidents resolved

1. The first switch preparation failed before downtime because an unprivileged `test -f` could not traverse the root-owned knowledge directory. The service and data were unchanged; the check was corrected to `sudo test`.
2. TASK-015B concurrently replaced the container after the first database switch, creating a temporary mixed state of new data with old routing code. The actual mount was rediscovered and only the five routing files were installed into TASK-015B.
3. Release knowledge paths were discovered to be shared symlinks. An attempted inactive-release restoration affected the shared active data. This was detected while the Gateway was stopped; the candidate was restored from the independent backup with temporary files plus atomic `mv`, hashes and inodes were rechecked, and the service was recreated healthy.

Final external verification after recovery confirmed 41 approved, 24 draft, 65 vectors, membership grounding, general answering and HTTP 422 draft protection. Two consecutive post-rollout snapshots of the final `...T095914Z` release showed the same routing hashes, data counts and healthy container state.
