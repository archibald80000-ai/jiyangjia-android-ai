# TASK-017: Design and build formal curated knowledge ingestion after pilot

- **Status:** PLANNED
- **Priority:** P2
- **Dependencies:** TASK-015
- **Branch:** `task/TASK-017-formal-knowledge-base-v1`
- **Owner:** Codex / assigned developer

## Objective

Design and build formal curated knowledge ingestion after pilot.

## Preconditions

- Store pilot passes
- Owner approves source governance and scope

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
3. Evaluate simple database/search versus vector/RAG based on real corpus and 4 GB server budget.
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
