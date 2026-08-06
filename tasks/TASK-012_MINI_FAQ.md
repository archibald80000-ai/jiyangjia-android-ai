# TASK-012: Implement lightweight RAG with SQLite, FAISS and source citations

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-011
- **Branch:** `task/TASK-012-mini-faq`
- **Owner:** Codex / assigned developer

## Objective

Implement the reviewed lightweight RAG layer using SQLite metadata, FAISS Top-K retrieval, document parsing and source citations.

## Preconditions

- TASK-011 is DONE
- A human-approved document/FAQ set is available or examples remain clearly labelled Mock/Draft
- TASK-011 EmbeddingProvider exists

## Scope and allowed changes

- `knowledge-test/`
- gateway knowledge module
- `tests/knowledge/`
- `docs/evidence/TASK-012/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Bulk scan of raw materials
- Dify, LangFlow, Flowise or external vector database service

## Detailed execution

1. Define and validate document/chunk schema, including status/source/review metadata.
2. Implement Markdown/TXT/PDF/DOCX parsing for explicitly selected files only.
3. Store document/chunk metadata in SQLite.
4. Build local FAISS index through the EmbeddingProvider.
5. Implement Top-K retrieval with source citations and approved-only customer answers.
6. Implement prohibited-topic and uncertain-answer transfer behavior before LLM fallback.
7. Create 20+ test cases covering approved, draft, rejected, unknown, medical, price and internal questions.
8. Do not scan or import the raw business directory.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/knowledge -q
```
```powershell
python scripts/evaluate_lightweight_rag.py --data knowledge-test
```

## Required deliverables

- [ ] Validated lightweight RAG engine
- [ ] Safety and evaluation report
- [ ] Clear Mock/approved content status

## Acceptance criteria

- [ ] Schema validation
- [ ] SQLite metadata
- [ ] FAISS Top-K retrieval
- [ ] Source citations
- [ ] Prohibited topics
- [ ] Safe transfer
- [ ] Evaluation report

## Stop / blocked conditions

- A destructive change, secret exposure, uncontrolled paid call or public network exposure would be required.
- A dependency is absent and cannot be safely installed inside the authorized scope.
- Real hardware/model/provider evidence is required but unavailable.
- Existing unrelated changes make safe staging impossible.

When blocked, complete all safe analysis, save sanitized evidence, set status to `BLOCKED` or `PARTIAL`, and state the exact unblock action.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Changed files and `git diff --stat`.
- Sanitized logs/screenshots where meaningful.
- Artifact paths and SHA-256 for APK/packages.
- Hardware/environment details for device/GPU claims.
- Failed cases, untested paths and cost-bearing calls.

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [ ] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [ ] Add evidence links/results to this task.
- [ ] Update `PROJECT_STATE.md`.
- [ ] Update `memory/CURRENT_STATE.md`.
- [ ] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [ ] Recommend exactly one next task.
