# TASK-011: Implement Mock and configurable LLM adapters

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-010
- **Branch:** `task/TASK-011-llm-router`
- **Owner:** Codex / assigned developer

## Objective

Implement Mock and configurable LLM adapters.

## Preconditions

- TASK-010 is DONE

## Scope and allowed changes

- `gateway/provider adapters`
- `integration/llm/`
- `tests/llm/`
- `docs/evidence/TASK-011/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Agent tools or autonomous actions

## Detailed execution

1. Implement deterministic Mock LLM for repeatable end-to-end tests.
2. Implement one OpenAI-compatible client abstraction with configurable base URL/model.
3. Add Doubao/Qwen provider configuration without coupling core business logic.
4. Enforce concise answer length, low creativity defaults and safe provider error handling.
5. Test streaming/non-streaming decision explicitly; do not add autonomous tools/actions.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/llm -q
```
```powershell
python scripts/test_llm_provider.py --provider mock --prompt "测试"
```

## Required deliverables

- [ ] LLM router and Mock
- [ ] At least one verified compatible provider when credentials permit
- [ ] Latency/token/cost-safe report

## Acceptance criteria

- [ ] Mock deterministic tests
- [ ] One OpenAI-compatible path
- [ ] Doubao/Qwen configuration slots
- [ ] Short-answer and safe-error policy

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
