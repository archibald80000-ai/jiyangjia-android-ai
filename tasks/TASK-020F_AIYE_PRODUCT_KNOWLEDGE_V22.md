# TASK-020F Aiye public product knowledge v2.2

## Goal

Publish the 25 user-authorized Aiye food HTML documents as a reviewable public source archive, build a detailed source-derived v2.2 Gateway package on top of v2.1, verify it with real Doubao Embedding/RAG, and release it to production with rollback evidence before merging through GitHub PR.

## Scope

- Read-only source: `E:\work\贝贝灵科技\0807-产品手册与网站展示\爱野食材(1)\爱野食材`.
- Public source archive: the 25 root HTML files only.
- Excluded: `.DS_Store`, `.workbuddy/`, env files, SQLite, FAISS, recordings and server backups.
- Existing v2.1 documents remain present; new IDs use the `aiye_` prefix.
- User confirmed all new source-derived records are human-reviewed and may be `approved`.

## Deliverables

- `knowledge-public/v2.2/` source archive, full package, dynamic import batches, manifest, source map, catalog and test set.
- Reproducible builder and structural tests.
- Isolated real-Embedding retrieval/dialogue acceptance evidence.
- Production backup, import, verification and rollback location.
- Updated project state, task board and handoff memory.

## Acceptance

- Exactly 25 HTML files are archived byte-for-byte with SHA-256.
- Every new document maps to a source file, source hash and section.
- Coverage includes 24 solar terms, 19 food-medicine ingredients and 11 Dayougu SKUs.
- Every import batch contains at most 50 documents and the batch union equals `import_all.json`.
- Real Doubao Embedding Top-3 acceptance is at least 90%, sources are 100% complete and draft leakage is zero.
- Representative real dialogue uses RAG/LLM/TTS and does not introduce facts outside retrieved sources.
- Production SQLite/FAISS is backed up before import and can be atomically restored.
- GitHub `main` contains the package and no prohibited secrets or runtime data.

## Status

`DONE / PRODUCTION_PUBLISHED` on 2026-08-09.

- Public package: 204 documents, including 65 preserved v2.1 documents and 139 new approved `aiye_` documents.
- Real Doubao Embedding: 340 vectors at 2048 dimensions.
- Local and production Top-3 acceptance: 240/240, sources 100%, draft leaks 0.
- Production real dialogue: 6 text flows and 1 synthetic-speech audio flow passed RAG/LLM/TTS or ASR/RAG/LLM/TTS.
- Production rollback: `/opt/jiyangjia-ai/backups/task020f-20260809T035803Z`.
- Evidence: `docs/evidence/TASK-020F/aiye-knowledge-v22-acceptance-20260809.md`.
- Public HTTPS remains separately blocked by TASK-014H; no Android physical-device result is claimed.
