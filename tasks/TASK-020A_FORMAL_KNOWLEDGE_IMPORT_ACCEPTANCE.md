# TASK-020A: Formal knowledge import acceptance

- **Status:** DONE
- **Priority:** P0
- **Dependencies:** TASK-017
- **Branch:** `task/TASK-020A-formal-knowledge-acceptance`

## Objective

Import and validate the reviewed Jiyangjia knowledge v2.1 package through the real Gateway RAG without modifying the source package, deleting demo FAQ records, exposing credentials, or treating Mock Embedding as production evidence.

## Safety boundary

- Source directory remained read-only: `E:\work\积养家\数字人知识库`.
- No source JSON, SQLite database, FAISS index, credential, recording, APK or media file is added to Git.
- The existing `var/task014a-dev/knowledge.db` and `faiss.index` were backed up and left active on port 18081.
- Port 8080 was not used. The acceptance Gateway listened only on `127.0.0.1:8090` and used an isolated candidate database.

## Result

- Real provider mode: Doubao Embedding through the configured `DOUBAO_API_KEY` fallback; 2048 dimensions. Dedicated `DOUBAO_EMBEDDING_API_KEY` and `ARK_API_KEY` were missing.
- Batch 1: 50 documents, 50 chunks, 50 vectors; 33 approved and 17 draft.
- Batch 2: 15 documents, 15 chunks; final state 65 documents, 65 chunks and 65 vectors; 41 approved and 24 draft.
- SQLite integrity: `ok`. FAISS: ready, 65 vectors, 2048 dimensions.
- Database version: curated corpus v2.1; the import package's JSON `version` field is `2`, and SQLite `PRAGMA user_version` is `0` because the current store has no numbered schema migration.
- Approved-document Top-1: 36/36. Draft targets excluded: 14/14. Safety cases: 24/24. General no-match cases: 6/6. Current-policy acceptance: 80/80 (100%).
- Sources contract: 80/80 complete, including 43/43 matched responses. Draft leaks: 0.
- Legacy exact-label comparison: 42/80 (52.5%) because the unchanged test file still expects draft documents to match and expects the superseded `safe_transfer` response status. This number is retained for audit and is not presented as the current policy score.

Evidence: `docs/evidence/TASK-020A/formal-knowledge-import-acceptance-20260807.md`.

## Completion boundary

TASK-020A proves the formal knowledge package and current retrieval policy on an isolated real-Embedding Gateway. ASR, TTS and LLM remained Mock on this knowledge-only process. It does not replace the active port-18081 demo database, deploy new data to Tencent Cloud, prove a full dialogue, or prove Android device behavior. The next task is to bind the accepted candidate or already activated formal server knowledge to the AI avatar demo and run a real voice dialogue without deleting the preserved demo database.
