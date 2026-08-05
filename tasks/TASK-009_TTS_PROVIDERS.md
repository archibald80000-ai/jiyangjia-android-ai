# TASK-009: Implement EdgeTTS then Doubao TTS adapters

- **Status:** PLANNED
- **Priority:** P1
- **Dependencies:** TASK-008
- **Branch:** `task/TASK-009-tts-providers`
- **Owner:** Codex / assigned developer

## Objective

Implement EdgeTTS then Doubao TTS adapters.

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

1. Implement deterministic test audio or Mock first, then EdgeTTS behind the common TTS interface.
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

- [ ] Mock/Edge/Doubao TTS adapters as actually available
- [ ] Audio metadata/checksum evidence
- [ ] Current API citation in task report

## Acceptance criteria

- [ ] Mock/test audio passes
- [ ] EdgeTTS integration
- [ ] Doubao contract verified from current official docs
- [ ] Timeout/error/cost guard
- [ ] Secrets remain server-side

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
