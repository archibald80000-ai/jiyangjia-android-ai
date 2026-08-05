# TASK-004: Automate and verify LiveTalking core control APIs

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-003
- **Branch:** `task/TASK-004-livetalking-api-contracts`
- **Owner:** Codex / assigned developer

## Objective

Automate and verify LiveTalking core control APIs.

## Preconditions

- TASK-003 has a running service or approved test endpoint

## Scope and allowed changes

- `scripts/test_livetalking_api.py`
- `integration/livetalking_client/`
- `tests/livetalking/`
- `docs/evidence/TASK-004/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Business LLM
- Formal knowledge base

## Detailed execution

1. Build a small test client against the locked upstream contract; do not change upstream behavior.
2. Establish/obtain a real session through `/offer` or `/whep`.
3. Test `/human` in echo mode before chat mode, then `/humanaudio` with a rights-cleared sample.
4. Test interrupt, speaking state, record start/end/download, action state and SSE start/end.
5. Use timeouts and clearly distinguish endpoint success from visible/aural rendering success.
6. Write a machine-readable result and human report; make repeated runs safe.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python scripts/test_livetalking_api.py --help
```
```powershell
python -m pytest tests/livetalking -q
```

## Required deliverables

- [ ] Reusable API test client
- [ ] Contract tests
- [ ] docs/evidence/TASK-004/api-contract-report.md

## Acceptance criteria

- [ ] /human echo
- [ ] /humanaudio
- [ ] /interrupt_talk
- [ ] /is_speaking
- [ ] /record
- [ ] /set_audiotype
- [ ] /sse

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
