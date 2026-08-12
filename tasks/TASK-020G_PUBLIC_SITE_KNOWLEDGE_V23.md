# TASK-020G Public site knowledge v2.3

## Goal

Publish the user-authorized public training site as a traceable knowledge package, extend the v2.2 corpus without deleting existing records, and make business-query routing data-driven so newly indexed products do not require source-code keyword edits.

## Source and scope

- Read-only source: `E:\work\积养家\积养家知识库\04_数字化系统\00_当前发布版\积养家AI知识库_Netlify直接上传包_V2.1_原页整合培训版`.
- Canonical public site: `https://jiyangjia-ai.netlify.app/`.
- Public repository package: `knowledge-public/v2.3/`.
- v2.2 remains the base; v2.3 adds 47 product records generated from `site/knowledge/index.json`.
- Runtime SQLite and FAISS files remain server-only and are never committed.

## Implementation

- Archive the 135 public site files with byte counts and SHA-256 in `manifest.json`.
- Generate the product documents from the site's structured `products[]` data rather than a hardcoded product list.
- Preserve all v2.2 IDs and statuses; assign new IDs with the `site_product_` prefix.
- Route explicit general-knowledge questions away from the business corpus, while allowing unknown product wording to enter business RAG when the current approved corpus has a strong lexical match.
- Keep approved-only customer retrieval, source citations and safe-transfer policy unchanged.

## Acceptance

- Package structure, unique IDs, source mapping and maximum document length pass automated tests.
- All batches contain at most 50 documents and their union equals `import_all.json`.
- Real Doubao Embedding produces a 2048-dimensional FAISS index.
- Product retrieval Top-3 rate is at least 90%, sources completeness is 100%, and draft leakage is zero.
- Production is backed up before import and can be restored atomically.
- One real production text dialogue returns a grounded answer, `request_id`, approved source, Doubao TTS `audio_id`, and downloadable audio.

## Status

`DONE / PRODUCTION_PUBLISHED` on 2026-08-12.

- Package: 251 documents, 227 approved, 24 draft.
- Vector state: 387 vectors at 2048 dimensions, real Doubao Embedding.
- Product search acceptance: 141/141 Top-3, sources 141/141, draft leaks 0.
- Production rollback: `/opt/jiyangjia-ai/backups/task-v23-production-20260812-024528`.
- Evidence: `docs/evidence/TASK-020G/public-site-knowledge-v23-acceptance-20260812.md`.
