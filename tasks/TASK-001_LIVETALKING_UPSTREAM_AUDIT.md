# TASK-001: Audit and pin the LiveTalking upstream source

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-000
- **Branch:** `task/TASK-001-livetalking-upstream-audit`
- **Owner:** Codex / assigned developer

## Objective

Audit and pin the LiveTalking upstream source.

## Preconditions

- TASK-000 is DONE
- Git and network access are available

## Scope and allowed changes

- `third_party/LiveTalking local ignored checkout`
- `config/upstream-lock.json only if evidence requires correction`
- `docs/evidence/TASK-001/`
- `docs/03_LIVETALKING_SCOPE.md`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Installing every model
- Android code

## Detailed execution

1. Run the deterministic bootstrap script and verify the exact locked SHA.
2. Record upstream remote, branch/detached state and clean status.
3. Read upstream README, LICENSE, API docs, config, app entry, route/session/avatar/TTS/LLM/plugin code relevant to this project.
4. Create an upstream audit: architecture, supported endpoints, model/assets, network ports, extension points, license/notice risks and differences from our desired architecture.
5. Do not install models or edit upstream source in this task.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```
```powershell
git -C third_party/LiveTalking rev-parse HEAD
```
```powershell
git -C third_party/LiveTalking status --short --branch
```
```powershell
git -C third_party/LiveTalking remote -v
```

## Required deliverables

- [ ] docs/evidence/TASK-001/upstream-audit.md
- [ ] Confirmed locked checkout
- [ ] Upstream compliance/extension summary

## Acceptance criteria

- [ ] Locked commit checked out
- [ ] Relevant README/API/config/source files summarized
- [ ] License/model/asset obligations recorded
- [ ] No upstream source changes

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
