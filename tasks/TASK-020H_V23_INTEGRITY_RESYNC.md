# TASK-020H Knowledge v2.3 integrity repair and v2.4 soup-story sync

## Goal

Preserve the published v2.3 release, repair deterministic package hashes, and append the two subsequently authorized soup-story HTML files as v2.4 without exposing unconfirmed menu or health wording to customer retrieval.

## Scope

- Read-only source: `E:\work\积养家\积养家知识库\04_数字化系统\00_当前发布版\积养家AI知识库_Netlify直接上传包_V2.1_原页整合培训版`.
- Preserved package: `knowledge-public/v2.3/`.
- Current package: `knowledge-public/v2.4/` with the two authorized HTML files archived byte-for-byte.
- Production knowledge: SQLite + FAISS mounted by the active Gateway release.
- No Android, Provider, Gateway API, Nginx or avatar changes.

## Acceptance

- All 135 authorized source files remain byte-for-byte identical to `knowledge-public/v2.3/site/`.
- Generated JSON uses deterministic UTF-8/LF bytes and every manifest size/hash matches the Git checkout.
- v2.4 preserves all 251 v2.3 documents and adds 15 draft records: two collection summaries and thirteen soup stories.
- Fresh-install batches contain 266 unique documents; the v2.3 upgrade delta contains only the 15 additions.
- GitHub `main` contains the repaired package and a rollback reference exists for the pre-task main commit.
- Production SQLite/FAISS is backed up before synchronization.
- Real production readiness, 141-case approved-product search, 43-case new-draft isolation, one dialogue/TTS/audio fetch and rollback evidence pass.
- Runtime databases, indexes, secrets, audio, APKs and server backups remain outside Git.

## Status

`DONE / PRODUCTION_PUBLISHED` on 2026-08-12.

- Production: 227 approved, 39 draft, 402 chunks/vectors at 2048 dimensions.
- Production backup: `/opt/jiyangjia-ai/backups/task020h-20260812T150643Z`.
- Server package: `/opt/jiyangjia-ai/knowledge-public/v2.4-6af1d79eb1f4-20260812T151153Z`.
- Evidence: `docs/evidence/TASK-020H/knowledge-v24-integrity-production-sync-20260812.md`.
