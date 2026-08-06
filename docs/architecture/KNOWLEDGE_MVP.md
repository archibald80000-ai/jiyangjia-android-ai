# Knowledge MVP

Updated: 2026-08-06

## Scope

Phase 1 knowledge is lightweight RAG, not a heavy knowledge platform. It uses FastAPI, SQLite, local FAISS, document parsers and an EmbeddingProvider. It does not use Dify, LangFlow or Flowise.

## Source Rules

- Only explicitly selected, human-reviewed Markdown/TXT/PDF/DOCX files may be indexed.
- Do not bulk scan `E:\work\积养家`.
- Every document and chunk has status: `approved`, `draft` or `rejected`.
- Customer-facing answers may use `approved` chunks only.
- Return `sources` and `request_id` for retrieval and dialogue responses.

## Retrieval Rules

- TASK-008 provides SQLite metadata and deterministic mock/keyword search.
- TASK-011 provides real EmbeddingProvider.
- TASK-012 adds FAISS Top-K vector retrieval and hybrid keyword fallback.

## Safety Rules

Do not invent:

- prices;
- inventory or appointment availability;
- activities, promotions or discounts;
- medical diagnosis, treatment effect or guarantee claims.

Unknown, low-confidence or sensitive questions must clearly transfer to staff.

## Acceptance

- SQLite schema and FAISS index are reproducible.
- Approved/draft/rejected status is enforced.
- Retrieval returns Top-K matches and sources.
- LLM prompt uses approved context only.
- Evaluation includes approved hit, draft exclusion, rejected exclusion, unknown fallback, price, medical and internal-data cases.
