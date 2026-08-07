# ADR-0010: Lightweight Admin Content and Display Layer

- Status: Accepted
- Date: 2026-08-07

## Decision

Build the Phase 1 management layer inside the existing FastAPI Gateway with server-rendered HTML, SQLite metadata and the existing SQLite/FTS5/FAISS/Embedding knowledge path. Use explicit publish transitions for knowledge and media, a public versioned asset manifest, and resolution-based Display Profile matching.

Production admin requests require a server-side `ADMIN_TOKEN`. No token is embedded in Android or page source.

## Consequences

- No Dify, CMS, frontend framework, RBAC or additional database service is required.
- Uploaded knowledge and assets remain draft until explicit publication.
- Android can consume stable manifest/profile contracts without a per-resolution APK.
- Production deployment, formal content approval and Android device validation remain separate work.
