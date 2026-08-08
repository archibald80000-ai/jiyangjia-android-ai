# TASK-020C production knowledge, avatar and sharing handoff

Executed: 2026-08-07 America/Chicago (`20260808T031244Z` UTC runtime stamp)

## Goal

Verify the production knowledge location, publish the user-approved portrait video and matching background to the Tencent Gateway, bind the default 1080x1920 Profile, document stable share URLs, and verify a real production dialogue without exposing private source paths.

## Decision

`PARTIAL / BLOCKED_BY_TENCENT_WEBBLOCK_ICP`.

Production knowledge, media, Profile and real Provider dialogue are complete and verified. Public sharing is not complete because external HTTPS is still reset before the request reaches Nginx. Server-local Nginx/TLS checks pass.

## Acceptance

- Production SQLite/FAISS paths and counts are recorded.
- Existing production admin/assets have a rollback backup.
- The source MOV remains unchanged and outside Git.
- Its 1080x1920 H.264 MP4 derivative and same-source JPG are uploaded, published and hash-verified after download.
- The default portrait Profile binds the new published asset IDs.
- Real RAG/LLM/TTS dialogue returns approved `knowledge://` sources and downloadable audio.
- README identifies share URLs and their current public availability honestly.

## Evidence

See `docs/evidence/TASK-020C/production-knowledge-avatar-sharing-20260807.md`.
