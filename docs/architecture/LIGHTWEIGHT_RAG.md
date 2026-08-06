# Lightweight RAG Architecture

Updated: 2026-08-06

## Decision

Phase 1 uses a lightweight local RAG module inside the FastAPI Gateway. It does not use Dify, LangFlow, Flowise, a managed vector database, or bulk ingestion of `E:\work\积养家`.

## Scope

- Input formats: Markdown, TXT, PDF, DOCX.
- Metadata store: SQLite.
- Vector index: local FAISS file, created in TASK-012.
- Embeddings: provider adapter using server-side environment variables.
- Retrieval: Top-K hybrid search, with keyword fallback and source citations.
- Answering: LLM receives only allowed retrieved context.

## Status Rules

- `approved`: can be used in customer-facing answers.
- `draft`: stored and searchable only for review/test flows.
- `rejected`: retained for audit but never used in answers.

## No-Claim Rules

The system must not invent prices, inventory, appointment availability, promotions, discounts, medical diagnosis, treatment effects, or guarantee claims.

When context is insufficient, the answer must say it cannot confirm the information and suggest asking staff.

## Data Model

SQLite tables planned for TASK-012:

- `documents(id, title, status, source_type, source_path, checksum, created_at, updated_at)`;
- `chunks(id, document_id, chunk_index, text, token_count, status)`;
- `embeddings(chunk_id, provider, model, dimensions, vector_ref, checksum)`;
- `ingestion_runs(id, request_id, status, document_count, chunk_count, error)`.

FAISS index files stay outside Git under runtime data, for example `var/knowledge/faiss.index`.

## Pipeline

```text
reviewed file
-> parse text
-> normalize and chunk
-> store document/chunks in SQLite
-> call EmbeddingProvider
-> write/update FAISS index
-> Top-K search returns chunks + sources
-> LLM answers with approved context only
```

## TASK Boundaries

- TASK-008: Gateway endpoints, provider contracts, SQLite skeleton, mock search.
- TASK-009: real Doubao TTS.
- TASK-010: real Doubao ASR.
- TASK-011: real LLM and Embedding provider adapter.
- TASK-012: document parsing, SQLite persistence, FAISS index, Top-K retrieval, source citation evaluation.
