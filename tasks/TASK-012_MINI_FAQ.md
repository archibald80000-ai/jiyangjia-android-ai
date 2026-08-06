# TASK-012: Implement lightweight RAG with SQLite, FAISS and source citations

- **Status:** DONE
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

- [x] Validated lightweight RAG engine
- [x] Safety and evaluation report
- [x] Clear Mock/approved content status

## Acceptance criteria

- [x] Schema validation
- [x] SQLite metadata
- [x] FAISS Top-K retrieval
- [x] Source citations
- [x] Prohibited topics
- [x] Safe transfer
- [x] Evaluation report

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

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## Completion evidence

- Branch: `task/TASK-012-mini-faq`
- Result: `DONE`
- Implemented SQLite metadata, SQLite FTS5 keyword index, FAISS Top-K vector index, explicit Markdown/TXT/PDF/DOCX ingestion, approved/draft/rejected status gates, prohibited-topic policy, safe transfer text and source citations.
- Added 10 approved demo FAQ entries, plus draft/rejected examples, under `knowledge-test/faq_mvp_approved.example.json`.
- Real Doubao/Ark embedding evaluation used private external env `E:\work\ai-kefu\.env.local`; secret values were not printed or committed.

Evidence files:

- `docs/evidence/TASK-012/lightweight-rag.md`
- `docs/evidence/TASK-012/task012-pytest-knowledge-20260806.txt`
- `docs/evidence/TASK-012/task012-pytest-full-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-mock-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-doubao-embedding-20260806.txt`
- `docs/evidence/TASK-012/task012-gateway-real-embedding-api-smoke-20260806.txt`

Verified commands:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge -q
```

Result: `6 passed, 1 warning`.

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q
```

Result: `34 passed, 1 warning`.

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test
```

Result: `ok=true`, `cases=24`, `passed=24`, `failed=0`.

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test --provider doubao --env-file E:\work\ai-kefu\.env.local
```

Result: `ok=true`, `cases=24`, `passed=24`, `failed=0`, real embedding dimensions `2048`.

Next action: execute exactly one next task, `TASK-013_END_TO_END_DIALOGUE.md`.
