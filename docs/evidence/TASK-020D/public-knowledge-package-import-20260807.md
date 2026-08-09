# TASK-020D public knowledge package and production import evidence

Executed: 2026-08-07 America/Chicago (`20260808T034524Z` UTC runtime stamp)

## Decision

`DONE`.

The user explicitly authorized the v2.1 knowledge in `E:\work\积养家\数字人知识库\08_导入包` for public GitHub sharing, employee learning and Gateway use. The original files remained read-only.

## Public package

Published repository directory: `knowledge-public/v2.1/`.

| File | Documents | Distribution | SHA-256 |
|---|---:|---|---|
| `import_all.json` | 65 | 41 approved / 24 draft | `2FCFE376FA686C48B5541CE5F3587FE3E72E438C5BCE346CBD6D95B878B2BBE3` |
| `import_batch_01.json` | 50 | 33 approved / 17 draft | `46F82250F0D5C0DC6DD2A231F79FFC4FA6FA96EE77961569486CC6D6EFB48024` |
| `import_batch_02.json` | 15 | 8 approved / 7 draft | `BDDF7D192A9811A9410D50EA888979F741CC5B78D4191E4120D31F040B56A2B9` |

The batch union equals `import_all.json`. IDs, titles, text and statuses are unchanged. All 65 workstation source paths were replaced with stable `knowledge://<document_id>` URIs. Files are emitted with deterministic LF line endings so Manifest hashes also match GitHub Raw downloads. No secret pattern, private key, API key assignment, Chinese ID number, email address or mobile number was found in the package audit.

## Production backup

Backup created before indexing:

`/opt/jiyangjia-ai/backups/task020d-public-knowledge-20260808T034524Z`

It contains an online SQLite backup, the pre-import FAISS index, pre-import status/hash evidence, both import responses, final validation and the 80-case summary. Directory permissions exclude group/other access.

## Real import

Active production paths:

- SQLite: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/jiyangjia.db`
- FAISS: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/faiss.index`

The 65-document complete body correctly returned HTTP 422 because the API limit is 50. No indexing occurred for that rejected request. The import then used the supported batches:

| Batch | HTTP | request_id | Indexed | Chunks | Elapsed |
|---|---:|---|---:|---:|---:|
| 01 | 200 | `task020d-batch-01` | 50 | 50 | 6533 ms |
| 02 | 200 | `task020d-batch-02` | 15 | 15 | 1711 ms |

Final validation:

- SQLite integrity: `ok`
- Documents: 65; approved 41; draft 24; rejected 0
- Chunks/embeddings/FAISS vectors: 65/65/65
- Embedding Provider: Doubao, 65 vectors at 2048 dimensions
- Stable `knowledge://` source URIs: 65; Windows source URIs: 0
- Content fingerprint SHA-256: `1D9EBD6DA8C454464CAF420D7C3E9FF4F9DEBE0889383FB223AEF31B795BE331`
- Final SQLite SHA-256: `DD25CA2E5102DA45330C0E1B45C5CC671C96392308D96BF557CD6253BF556F97`
- Final FAISS SHA-256: `D3F43449155D04F333032601AD58D5CB7E8B5D3C5C67F1E6CE034AD4D648ED40`

## Eighty-case production search

All 80 cases called the production-local `POST /api/v1/knowledge/search` and therefore used the real Doubao Embedding configuration.

| Gate | Result |
|---|---:|
| Approved target ranked Top-1 | 36/36 |
| Draft target remained hidden | 14/14 |
| Safety/transfer intent remained safe | 24/24 |
| General intent returned no business match | 6/6 |
| Current-policy correctness | 80/80 (100%) |
| Endpoint returned `matched` | 43/80 |
| Sources contract complete | 80/80; matched 43/43 |
| Draft leaks | 0 |
| No-match responses | 37 |

The unchanged legacy exact-label score remains 42/80 because it expects draft documents to be customer-visible and expects the superseded `safe_transfer` response label. This is recorded separately and is not used to weaken the approved/draft publication policy.

## Verification

Focused local tests before publication:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge\test_public_knowledge_package.py tests\knowledge\test_lightweight_rag.py -q
```

Result: 13 passed with one third-party FAISS/NumPy deprecation warning.

The public package is the GitHub/employee sharing surface. The production SQLite and FAISS files remain server-only runtime data.
