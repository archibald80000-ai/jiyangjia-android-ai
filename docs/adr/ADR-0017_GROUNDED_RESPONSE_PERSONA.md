# ADR-0017: Separate grounded retrieval from response persona

Status: Accepted

Date: 2026-08-12

## Context

Production retrieval was accurate and source-complete, but a defensive single prompt and 240-character excerpts made answers repetitive. Story-shaped requests also caused the active Doubao model to enter deep-thinking generation and exceed the 30-second real-time timeout.

## Decision

- SQLite/FTS/FAISS remains responsible only for approved fact retrieval and source traceability.
- A versioned persona layer controls tone, response rhythm and TTS-friendly wording after retrieval.
- Query rewriting may remove conversational wrappers and add intent terms, but it must not lower retrieval thresholds or expose draft documents.
- The answer stage may hydrate only approved matched chunks and must keep the public search response bounded.
- Doubao/Ark real-time Chat requests explicitly set `thinking.type=disabled`.
- Deterministic post-generation guards remove unsupported current-inventory and medical-treatment promises.

## Consequences

- Knowledge and vectors do not need rebuilding for tone changes.
- Persona changes are testable and versioned independently from knowledge releases.
- Long-term customer memory remains out of scope; the current persona is stateless per request.
- Human tone review remains useful even when factual and safety tests pass.
