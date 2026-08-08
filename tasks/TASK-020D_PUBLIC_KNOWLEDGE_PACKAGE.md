# TASK-020D public knowledge package and production re-import

Executed: 2026-08-07 America/Chicago (`20260808T034524Z` UTC runtime stamp)

## Goal

Publish the user-authorized v2.1 customer-facing knowledge as a reviewable GitHub JSON package, import the same content into the current Tencent Gateway with real Doubao Embedding, and verify approved/draft isolation plus source citations.

## Decision

`DONE`.

## Scope and safety

- Source directory remained read-only: `E:\work\积养家\数字人知识库\08_导入包`.
- Public copies preserve IDs, titles, text and statuses.
- Workstation source paths are replaced with `knowledge://<document_id>`.
- SQLite, FAISS, original PDF/DOCX, provider secrets and media are not committed.
- The current Gateway accepts at most 50 documents per request, so production import used the 50-document and 15-document batches.

## Acceptance

- Public package: 65 documents, 41 approved and 24 draft.
- Production: 65 chunks and 65 real Doubao vectors at 2048 dimensions.
- SQLite integrity: `ok`; all 65 source URIs use `knowledge://`.
- Content fingerprint matches the authorized package.
- Current-policy search acceptance: 80/80; draft leaks: 0; sources complete: 80/80.
- Rollback backup exists before the re-import.

## Evidence

See `docs/evidence/TASK-020D/public-knowledge-package-import-20260807.md`.
