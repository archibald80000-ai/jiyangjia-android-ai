# TASK-009: Implement Doubao TTS adapter

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-008
- **Branch:** `task/TASK-009-tts-providers`
- **Owner:** Codex / assigned developer

## Objective

Implement Mock/test TTS and Doubao TTS adapters for the Phase 1 MVP.

## Preconditions

- TASK-008 is DONE
- Provider credentials, if used, are stored outside Git

## Scope and allowed changes

- `gateway/provider adapters`
- `integration/tts/`
- `tests/tts/`
- `docs/evidence/TASK-009/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Voice cloning

## Detailed execution

1. Implement deterministic test audio or Mock first behind the common TTS interface.
2. Research the current official Doubao/Volcengine TTS API and record exact source/date before implementation.
3. Implement Doubao TTS with server-side credentials, format normalization and voice configuration.
4. Add timeout, finite retry, provider error mapping and small cost-controlled integration tests.
5. Verify Android-playable output and never log authorization data.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/tts -q
```
```powershell
python scripts/test_tts_provider.py --provider edge --text "您好"
```
```powershell
python scripts/test_tts_provider.py --provider doubao --text "您好"
```

## Required deliverables

- [x] Mock/Doubao TTS adapters as actually available
- [x] Audio metadata/checksum evidence
- [x] Current API citation in task report

## Acceptance criteria

- [x] Mock/test audio passes
- [x] Doubao contract verified from current official docs
- [x] Timeout/error/cost guard
- [x] Secrets remain server-side
- [ ] Real Doubao TTS call succeeds with approved credentials

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

## TASK-009 Result

- Doubao TTS adapter code is implemented behind the common TTS Provider interface.
- Mock TTS CLI returned deterministic audio bytes, SHA-256 `248253DDDE4121C7512AF5E387BAAEC4EE48C7530D0EAB16F03A31D5DBFC9427`.
- Unit tests passed: `python -m pytest tests\tts tests\gateway -q` -> 7 passed.
- Follow-up Gateway missing-credential regression test passed: 8 tests passed.
- Follow-up config preflight and redaction tests passed: 9 tests passed.
- Real Doubao CLI path correctly returns `BLOCKED_PROVIDER_CREDENTIALS`.
- Doubao config preflight returns only `configured/missing` status and does not print values.
- `.env.example` now uses the current TASK-009 variable names and placeholder values only.
- Latest blocker recheck still returns `BLOCKED_PROVIDER_CREDENTIALS`; no real Doubao TTS success is claimed.
- Real Doubao TTS audio was not generated because credentials are missing:
  - `DOUBAO_TTS_APP_ID`
  - `DOUBAO_TTS_ACCESS_TOKEN`
  - `DOUBAO_TTS_VOICE_TYPE`
- Evidence: `docs/evidence/TASK-009/tts-provider.md`.
