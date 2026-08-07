# TASK-017: Design and build formal curated knowledge ingestion after pilot

- **Status:** PARTIAL
- **Priority:** P2
- **Dependencies:** TASK-015
- **Branch:** `task/TASK-017-formal-knowledge-base-v1`
- **Owner:** Codex / assigned developer

## Objective

Design and build formal curated knowledge ingestion after pilot.

## Preconditions

- Store pilot passes
- Owner approves source governance and scope

The user explicitly authorized the audited v2.1 import package and 80-case evaluation on 2026-08-07. This authorizes the isolated import/evaluation below but does not waive the 90% activation gate or authorize production deployment.

## Scope and allowed changes

- `New formal knowledge modules/docs approved by this task`
- `docs/evidence/TASK-017/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Unreviewed bulk import

## Detailed execution

1. Inventory candidate sources without modifying originals and classify sensitivity/authority/version.
2. Define approval, extraction, chunking, update, expiry and deletion workflow.
3. Evaluate simple database/search versus vector/RAG based on real corpus and the observed small server budget.
4. Build a reviewed evaluation set and citation/audit requirements before production ingestion.
5. Implement the chosen small, reversible V1 and document resource/quality results.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
Task-specific after architecture approval; no bulk command is authorized by default.
```

## Required deliverables

- [ ] Approved source inventory
- [ ] Knowledge governance and architecture ADR
- [ ] Measured retrieval evaluation

## Acceptance criteria

- [ ] Approved source inventory
- [ ] Update/review workflow
- [ ] Retrieval evaluation
- [ ] Citation/audit
- [ ] Resource/deployment decision

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

## v2.1 import attempt (2026-08-07)

- Verified `import_batch_01.json` (50), `import_batch_02.json` (15), `import_all.json` (65) and 80 test cases without modifying the source directory.
- Used the external ignored provider configuration only by configured/missing status; no value was printed or committed. Real Doubao/Ark Embedding was ready.
- Created a consistent SQLite online backup plus FAISS backup before import.
- Imported an isolated, empty v2.1 candidate on port 8090: 65 documents, 65 chunks, 65 real 2048-dimensional embeddings; 41 approved and 24 draft.
- Customer-visible search kept draft documents excluded, but the 80-case suite passed only 51/80 (63.75%), below the required 90%.
- Activation was refused. The task-created 8090 process was stopped, the candidate was marked `FAILED-63.75pct`, and the existing 18081 database remained unchanged.
- Detailed evidence: `docs/evidence/TASK-017/knowledge-v2.1-import-evaluation-20260807.md`.

## Owner decision and scoped-routing verification (2026-08-07)

- Owner replaced the old blanket-transfer policy: explicit 积养家/product/service questions require approved evidence and fail closed when none exists; other questions receive a contextual general answer.
- Decision recorded in `docs/adr/ADR-0014_KNOWLEDGE_SCOPED_ANSWER_ROUTING.md`.
- Removed pre-retrieval medical/price/internal keyword rejection, added business/general scope routing, draft-shadow protection and stricter evidence scoring.
- Locked the public search request model to `include_draft=false`; an explicit `true` request is rejected with HTTP 422 while internal admin preview remains available.
- Real v2.1 retrieval: approved target top-1 `36/36`; draft target exclusion `14/14`; six general questions bypassed business search `6/6`; unknown 积养家 product returned no match.
- Real Doubao LLM checks passed for approved grounding, unknown-business refusal, general writing and general health guidance.
- TASK-017 regression: `47 passed, 1 unrelated TASK-015A test deselected`; full repository excluding that same assertion: `84 passed`.
- Candidate remains isolated on localhost 8090. Production and the existing 18081 database were not switched, so the task remains `PARTIAL` rather than `DONE`.
- Detailed evidence: `docs/evidence/TASK-017/knowledge-routing-v2.1-20260807.md`.
