# TASK-020E Gateway real v2.1 import acceptance

Executed: 2026-08-08 America/Chicago (`20260808T055957Z` UTC runtime stamp)

## Decision

`READY_FOR_DEMO`.

The authorized v2.1 package was imported into a new local candidate with all four real Providers. Existing demo data and the prior accepted candidate were preserved. This result is not Android physical-device, human microphone, public HTTPS or long-run store evidence.

## Gateway configuration

- URL: `http://127.0.0.1:8091`
- SQLite: `var/task020e/20260808T055957Z/candidate/knowledge.db`
- FAISS: `var/task020e/20260808T055957Z/candidate/faiss.index`
- ASR: Doubao, ready
- TTS: Doubao, ready
- LLM: Doubao/Ark-compatible, ready
- Embedding: Doubao, ready; `doubao-embedding-vision-251215` default path
- Knowledge: SQLite + FTS5 + FAISS

The protected external env was read only by the process. Credential values were never printed, copied or committed. Provider selection was explicitly set in the child process because the private env intentionally does not persist runtime Provider choices.

## Preservation and rollback

Backup directory:

`var/task020e/20260808T055957Z/backups/pre-import/`

It contains online SQLite backups and FAISS copies for:

- port-18081 Mock demo: 2 approved / 1 draft / 1 rejected
- port-18084 previous real candidate: 41 approved / 24 draft

Both backup SQLite files passed `PRAGMA integrity_check=ok`. Port 18081 remained at 2/1/1 after TASK-020E; no demo FAQ or old index was deleted.

## Import

`import_all.json` was not submitted. The supported batches were posted in order:

| Batch | HTTP | request_id | Indexed | Chunks | Elapsed |
|---|---:|---|---:|---:|---:|
| `import_batch_01.json` | 200 | `task020e-import-01` | 50 | 50 | 9020.1 ms |
| `import_batch_02.json` | 200 | `task020e-import-02` | 15 | 15 | 2443.0 ms |

Final database/index validation:

- Documents: 65
- Approved/draft/rejected: 41/24/0
- Chunks/embeddings/vectors: 65/65/65
- Embedding Provider: Doubao, 65 x 2048
- SQLite integrity: `ok`
- Stable `knowledge://` sources: 65/65
- Content fingerprint: `1D9EBD6DA8C454464CAF420D7C3E9FF4F9DEBE0889383FB223AEF31B795BE331`
- SQLite SHA-256: `31DB666B929C24DE1F3EFFF072749F29A7AA733FCB6E5708938559127B2CA738A`
- FAISS SHA-256: `0D3F75E8C8EB5D065D972B7C186D689499839602937CC098D39E65FF09D745D5`

## Eighty-case search

All 80 cases called `POST /api/v1/knowledge/search` with real Doubao Embedding and `top_k=3`.

| Metric | Result |
|---|---:|
| Endpoint matched rate | 43/80 (53.75%) |
| Approved target Top-1 | 36/36 (100%) |
| Approved target Top-3 | 36/36 (100%) |
| Current-policy pass rate | 80/80 (100%) |
| Sources complete | 80/80; matched 43/43 |
| Draft leaks | 0 |
| Controlled no-match | 37 |

The unchanged legacy exact-label result remains 42/80 because it expects draft content to be returned and expects a superseded response label. It is not the publication-policy acceptance metric.

## Real dialogue acceptance

Each question was first synthesized into MP3 by real Doubao TTS, then uploaded to `/api/v1/dialogue/audio`. This exercises real Doubao ASR -> SQLite/FAISS RAG -> Doubao LLM -> Doubao TTS and audio download, but it is synthetic speech rather than a human microphone recording.

The first pass was 2/5. Three failures exposed two specific application gaps:

- ASR returned `漆扇鸡汤`; scoped soup-context normalization now maps it to `七膳鸡汤`.
- The short kiosk intents `有什么产品` and `怎么体验` needed narrow retrieval expansions.

No knowledge document, status, threshold or vector was changed. After the scoped code correction, the same three MP3 inputs were reused and final acceptance was 5/5.

| Question | ASR/RAG result | Approved source | Result |
|---|---|---|---|
| 积养家是什么？ | `机养家` normalized to `积养家`; matched | `faq_brand_002`, `faq_brand_001`, `faq_food_001` | PASS |
| 有什么产品？ | matched | `faq_service_007` | PASS |
| 七膳鸡汤是什么？ | `漆扇` normalized to `七膳`; matched | `faq_soup_005` | PASS |
| 门店在哪里？ | no-match because location is draft | none; safely asks staff | PASS |
| 怎么体验？ | matched | `faq_scenario_001` | PASS |

All five responses reported real Doubao ASR/LLM/TTS, returned HTTP 200, produced downloadable `audio/mpeg`, and had complete `knowledge://` sources when matched.

Example answers:

- `有什么产品？` -> “我们有一些智能康养产品，您可以免费上手体验，也能先租回家用，觉得好再买……”
- `门店在哪里？` -> “门店位置的相关信息我暂时没法确认，您可以咨询现场工作人员了解。”
- `怎么体验？` -> “您先进门坐下来喝杯免费姜茶，告诉我您想体验什么；买不买都一样热情。”

## Runtime evidence

Ignored evidence remains under:

`var/task020e/20260808T055957Z/candidate/`

It includes import/status JSON, final database validation, both 80-case summaries, first/final dialogue summaries, generated test MP3 files and Gateway logs. Audio, SQLite, FAISS and raw question results are not committed.
