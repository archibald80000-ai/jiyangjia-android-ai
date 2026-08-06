# TASK-011: Implement real LLM and Embedding adapters

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-010
- **Branch:** `task/TASK-011-llm-router`
- **Owner:** Codex / assigned developer

## Objective

Implement real LLM and Embedding adapters behind the Provider interfaces.

## Preconditions

- TASK-010 is DONE
- TASK-008 Provider interfaces exist

## Scope and allowed changes

- `gateway/provider adapters`
- `integration/llm/`
- `integration/embedding/`
- `tests/llm/`
- `docs/evidence/TASK-011/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Agent tools or autonomous actions
- RAG document parsing/indexing; that belongs to TASK-012

## Detailed execution

1. Verify current official Doubao/Volcengine Ark LLM and embedding API documentation before implementation.
2. Implement OpenAI-compatible chat client abstraction with configurable base URL/model.
3. Implement Doubao/Volcengine Ark LLM configuration and one real bounded test when credentials permit.
4. Implement EmbeddingProvider abstraction and one real embedding path when credentials permit.
5. Enforce concise answer length, low creativity defaults and safe provider error handling.
6. Test streaming/non-streaming decision explicitly; do not add autonomous tools/actions.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/llm -q
```
```powershell
python scripts/test_llm_provider.py --provider mock --prompt "测试"
```

## Required deliverables

- [x] LLM router and Mock/real adapters
- [x] Embedding adapter
- [x] At least one verified compatible LLM provider when credentials permit
- [x] Latency/token/cost-safe report

## Acceptance criteria

- [x] Mock deterministic tests
- [x] One OpenAI-compatible path
- [x] Doubao/Volcengine Ark configuration slots
- [x] Embedding API path
- [x] Short-answer and safe-error policy
- [ ] Real Embedding API call accepted by provider/account

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

## TASK-011 close-out result

Updated: 2026-08-06

Status: `PARTIAL`.

Completed:

- Added `OpenAICompatibleLLMProvider` and `OpenAICompatibleEmbeddingProvider`.
- Added DeepSeek, Doubao/Ark and generic OpenAI-compatible configuration slots.
- Added CLI smoke tools and 8 TASK-011 tests.
- Verified full backend regression: 25 tests passed.
- Verified real DeepSeek LLM call with private external env; usage metadata was present.
- Verified real Doubao/Volcengine Ark LLM call with private external env; usage metadata was present.
- Verified Doubao/Ark Embedding configuration preflight; values were not printed.

Not completed:

- Real Doubao/Ark Embedding call was rejected by the provider with sanitized
  error `http_status=404`, `provider_code=InvalidEndpointOrModel.NotFound`.

Evidence:

- `docs/evidence/TASK-011/llm-provider.md`
- `docs/evidence/TASK-011/task011-pytest-final-20260806.txt`
- `docs/evidence/TASK-011/task011-deepseek-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-real-call-rejected-20260806.txt`

Next required unblock before TASK-012:

- Configure an enabled Ark/Doubao embedding model or endpoint in private env,
  then rerun `scripts/test_embedding_provider.py --provider doubao`.
