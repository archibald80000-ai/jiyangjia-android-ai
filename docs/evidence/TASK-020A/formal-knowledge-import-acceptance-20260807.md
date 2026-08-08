# TASK-020A formal knowledge import acceptance

Executed: 2026-08-07 America/Chicago (`20260808T023610Z` UTC runtime stamp)

## Decision

`DONE` for isolated formal knowledge import acceptance.

The current approved retrieval policy passed 80/80 with real Doubao Embedding. The existing local demo database was preserved and was not switched. This evidence does not claim a production deployment or Android device result.

## Environment

Project `E:\work\ai-kefu\jiyangjia-ai\.env.local` status:

- `DOUBAO_API_KEY`: missing
- `DOUBAO_EMBEDDING_API_KEY`: missing
- `ARK_API_KEY`: missing
- `JIYANGJIA_KNOWLEDGE_DB_PATH`: missing

Protected external provider file `E:\work\ai-kefu\.env.local` status:

- `DOUBAO_API_KEY`: configured
- `DOUBAO_EMBEDDING_API_KEY`: missing
- `ARK_API_KEY`: missing
- `JIYANGJIA_KNOWLEDGE_DB_PATH`: missing

No value was printed or copied. The Gateway used the supported Doubao Embedding credential fallback and explicit process-only candidate paths.

## Existing state and backup

The existing port-18081 demo Gateway remained at 2 approved, 1 draft and 1 rejected document with Mock Embedding. Its four documents do not overlap the 65-document v2.1 package, so importing into that same database could not satisfy the required exact 41/24 distribution without deleting demo records.

Required rollback files:

- `var/task014a-dev/knowledge.db.backup.20260808T023610Z`
  - SQLite online backup integrity: `ok`
  - SHA-256: `5C84A79701A4EA6F50FAA17201B6D6F5CA2A350BC37E1B1073BECFB0913A1FF2`
- `var/task014a-dev/faiss.index.backup.20260808T023610Z`
  - SHA-256: `0F6B3A25F95649A268384CECA3557EAD5ADE7A341B5AFA94DEC4923A35DF5497`

These files are ignored runtime artifacts and are not committed.

## Isolated Gateway

- URL: `http://127.0.0.1:8090`
- Candidate runtime: `var/task014a-dev/task020a-candidate-20260808T023610Z/`
- Embedding provider: `doubao`
- Initial state: 0 documents, 0 chunks, 0 vectors
- Port 8080 was not used.

## Import

| Batch | HTTP | Indexed | Chunks | Distribution | FAISS |
|---|---:|---:|---:|---|---|
| `import_batch_01.json` | 200 | 50 | 50 | 33 approved / 17 draft | 50 x 2048 |
| `import_batch_02.json` | 200 | 15 | 15 | final 41 approved / 24 draft | 65 x 2048 |

Final candidate state:

- Documents: 65
- Chunks: 65
- Embeddings: 65
- Database version: curated corpus v2.1; JSON package `version=2`; SQLite `PRAGMA user_version=0`
- SQLite integrity: `ok`
- Candidate SQLite SHA-256: `30464126AFF59CD1F5E39DC95D6CEE6DC045C8F19B06F08E4FEA6E4A50674AE9`
- Candidate FAISS SHA-256: `89793A680F72DBB0FEF7991523716382AF2A89A0633FBADB732527CCBFE7D39F`

## Eighty-case search acceptance

All 80 cases called `POST /api/v1/knowledge/search` with real Doubao Embedding.

| Gate | Result |
|---|---:|
| Approved expected document ranked Top-1 | 36/36 |
| Draft expected document excluded | 14/14 |
| Safety/transfer intent remained safe | 24/24 |
| General intent returned no business match | 6/6 |
| Current-policy correctness | 80/80 (100%) |
| Endpoint returned `matched` | 43/80 (53.75%) |
| Sources contract complete | 80/80; matched responses 43/43 |
| Draft leaks | 0 |
| No-match responses | 37 |

No-match case IDs:

`t007, t015, t016, t017, t018, t019, t025, t026, t027, t028, t029, t032, t044, t052, t056, t057, t059, t060, t061, t062, t063, t064, t065, t066, t067, t068, t069, t070, t071, t073, t074, t075, t076, t077, t078, t079, t080`.

The unchanged test file's legacy exact-label comparison is 42/80 (52.5%). It expects 14 draft documents to be customer-visible and expects 24 requests to return the superseded `safe_transfer` status. Current acceptance instead requires draft isolation and accepts an approved safety-boundary source or no match for those safety requests. Both results are recorded to avoid concealing the contract difference.

Detailed responses, questions and local databases remain only in ignored runtime state:

- `var/task014a-dev/task020a-candidate-20260808T023610Z/evaluation-80-raw.json`
- `var/task014a-dev/task020a-candidate-20260808T023610Z/evaluation-80-summary.json`

The raw report SHA-256 is `07198A6ED69F56996768A8D670EB522C03A5C845625FAB0F31D50AA650FF5D9D`.

## Verification commands

The credential file was passed only as a path and no value was emitted:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config

# The child process loaded the protected env internally, then received explicit
# JIYANGJIA_EMBEDDING_PROVIDER=doubao and candidate DB/FAISS paths.
.\.venv\gateway-task008-py310\Scripts\python.exe -m gateway --host 127.0.0.1 --port 8090

# Each source file was parsed locally and posted without copying it into Git.
POST http://127.0.0.1:8090/api/v1/knowledge/index
GET  http://127.0.0.1:8090/api/v1/knowledge/status
POST http://127.0.0.1:8090/api/v1/knowledge/search

.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest -q
powershell -ExecutionPolicy Bypass -File scripts\verify_repository.ps1
```

Results:

- Full pytest: 88 passed, 1 third-party FAISS/NumPy deprecation warning.
- Repository verification: PASS.
- JSON/YAML validation: PASS.
- Public `include_draft=true`: HTTP 422.
- Source files retained their original timestamps and post-run SHA-256 values.
- Candidate readiness reported real Doubao Embedding; ASR/TTS/LLM were intentionally Mock for this knowledge-only task.

## Completion boundary

The formal knowledge package is suitable for the next AI avatar dialogue integration gate. Port 18081 still uses the preserved demo database, and port 8090 is an isolated knowledge acceptance Gateway with only Embedding configured as real. A later task must bind the accepted candidate or the already activated formal server knowledge to a Gateway with real ASR/LLM/TTS and verify ASR -> RAG -> LLM -> TTS without replacing the preserved demo database.
