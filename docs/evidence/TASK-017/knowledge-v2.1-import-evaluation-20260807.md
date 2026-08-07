# Knowledge v2.1 isolated import and evaluation — 2026-08-07

## Decision

`PARTIAL / NOT ACTIVATED`. Real Embedding import succeeded, but customer-search evaluation was `51/80 = 63.75%`, below the required 90%. The existing local active database and the production Gateway were not switched.

## Environment decision

- Selected path A with isolation.
- Project `.env.local`: absent.
- External ignored provider configuration: present; Doubao Embedding configuration check returned ready. No secret values were read into evidence, printed or committed.
- Persistent database variables were absent, so the candidate process received explicit versioned SQLite/FAISS paths.
- Stable runtime: `.venv/gateway-task008-py310`, Python 3.10.11.
- Port 8080 was occupied by `ApplicationWebServer`; port 8090 was used and later stopped.

## Source audit

- Source directory remained read-only: `E:\work\积养家\数字人知识库`.
- Batch 1: 50 documents, 33 approved, 17 draft.
- Batch 2: 15 documents, 8 approved, 7 draft.
- Full package: 65 unique IDs, 41 approved, 24 draft.
- Test set: 80 cases: 50 matched, 24 safe_transfer, 6 no_match.

The pre-existing `var/task014a-dev/knowledge.db` contained 4 documents, not the reported 10, and none of their IDs overlapped the v2.1 package. A fresh versioned candidate was therefore used to preserve the old database while meeting the exact 65-document acceptance count.

## Backup

- Directory: `var/knowledge-backups/pre-v2.1-20260807-034811/` (ignored runtime state).
- SQLite online backup: integrity `ok`, 4 documents, SHA-256 `CEFA70A674965FE30FF5C2A4F2CBFD3FDE36EDB7DDB32784869C74E7CD267B04`.
- FAISS backup: SHA-256 `0F6B3A25F95649A268384CECA3557EAD5ADE7A341B5AFA94DEC4923A35DF5497`.

## Import result

- Batch 1: HTTP 200, indexed 50, chunks 50, 50 embeddings, 2048 dimensions.
- Batch 2: HTTP 200, indexed 15, final documents 65, chunks 65, embeddings 65, vectors 65, 2048 dimensions.
- Final distribution: 41 approved, 24 draft, 0 rejected.
- Candidate SQLite integrity: `ok`.
- Candidate database SHA-256: `E8C744E4D2887A74D37CB23768390D449BE582B51D131ECA03D09D11EA834BCE`.
- Candidate FAISS SHA-256: `BE2E0969248B1020C04B6C6862C6A3CE0C5C50FAED1115657489516A70995B6C`.

## Evaluation result

| Expected result | Passed | Total |
|---|---:|---:|
| matched | 36 | 50 |
| safe_transfer | 12 | 24 |
| no_match | 3 | 6 |
| **Total** | **51** | **80** |

Pass rate: **63.75%**.

Root-cause split:

1. All 36 matched cases whose expected document was approved passed. The remaining 14 matched cases expected draft document IDs, which conflicts with the required customer endpoint behavior `include_draft=false`.
2. The safe-transfer classifier covered only 12/24 expected cases. Medical-effect, customer-record, internal-business, delivery and similar questions need reviewed policy coverage.
3. Three out-of-domain questions incorrectly matched approved documents, showing that the current similarity/keyword acceptance threshold needs a no-answer guard.
4. One draft price case expected a match while the existing global price policy correctly forced safe transfer; the test expectation and publication policy must be reconciled by the owner.

The detailed sanitized case report is retained at ignored runtime path:
`var/knowledge-releases/v2.1-20260807-034811-FAILED-63.75pct/evaluation-80.json`, SHA-256 `2905E8BBAAA0B1A7A07826495E0F72D476DC8415337A9F6110A6D3244365E82D`.

## Rollback / active state

- Candidate Gateway PID was stopped and port 8090 is no longer listening.
- Failed candidate retained at `var/knowledge-releases/v2.1-20260807-034811-FAILED-63.75pct/` for audit; it is not active.
- Existing port 18081 status after rollback remained 2 approved, 1 draft, 1 rejected, 2 embeddings.
- No production server, port 8080 service, source JSON, active SQLite or active FAISS file was overwritten.

## Required next action

Reconcile the 14 draft-dependent expected matches with publication status, extend safe-transfer policy coverage, and add an out-of-domain rejection gate. Re-run the same 80 cases with unchanged thresholds; activate only at 90% or higher.
