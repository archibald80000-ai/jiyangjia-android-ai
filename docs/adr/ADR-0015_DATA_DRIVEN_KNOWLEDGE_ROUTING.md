# ADR-0015: Data-driven knowledge routing

- Status: Accepted
- Date: 2026-08-12

## Context

The business-query classifier originally depended on a small static list of brand and product terms. Newly published products could be indexed correctly in SQLite/FAISS but still be classified as general knowledge before retrieval, requiring a code deployment for each product name.

## Decision

Keep explicit general-knowledge intents outside the business corpus. For otherwise unknown queries, probe the current approved SQLite/FTS corpus. A strong lexical match routes the query to the business RAG as `dynamic_corpus`, after which the existing hybrid FTS/FAISS Top-K search, approved-only gate and source contract apply.

Product records and aliases are generated from the versioned public package's structured data. Product names are not maintained in application source code.

## Consequences

- New reviewed products normally require a data package build and re-index, not a Python keyword edit.
- Explicit general questions and weak/no-match questions retain their existing safe routing behavior.
- Draft and rejected records do not become customer-visible routing evidence.
- The lexical threshold and approved-only policy remain regression-tested because overly broad matches could misroute general questions.
