# TASK-013: Connect Android, gateway, providers and both display modes

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-012
- **Branch:** `task/TASK-013-end-to-end-dialogue`
- **Owner:** Codex / assigned developer

## Objective

Connect Android, gateway, providers and the idle-video voice FAQ mode.

## Preconditions

- TASK-005/007/008/009/010/011/012 satisfy their required interfaces

## Scope and allowed changes

- `android-app/`
- `gateway/`
- `integration/`
- `tests/e2e/`
- `docs/evidence/TASK-013/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Production scale

## Detailed execution

1. Connect one interaction request across Android/gateway/ASR/knowledge-or-LLM/TTS and playback.
2. Propagate one request ID through every component and state transition.
3. Validate idle-video voice mode.
4. Test interrupt/cancel, provider timeout and network loss.
5. Run 30 controlled cycles and report failures, latency breakdown and fallback count.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/e2e -q
```
```powershell
.\android-app\gradlew.bat -p android-app connectedDebugAndroidTest
```

## Required deliverables

- [ ] End-to-end demonstrable loop
- [ ] 30-cycle stability/latency report
- [ ] Fallback evidence

## Acceptance criteria

- [ ] Audio → ASR → answer → TTS → playback works
- [ ] Idle-video fallback works
- [ ] Request ID correlation
- [ ] 30-cycle stability test

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
