# TASK-016: Evaluate MuseTalk after the Wav2Lip pilot baseline

- **Status:** DEFERRED
- **Priority:** P2
- **Dependencies:** TASK-015
- **Branch:** `task/TASK-016-musetalk-evaluation`
- **Owner:** Codex / assigned developer

## Objective

Evaluate MuseTalk after the Phase 1 MVP and any resumed LiveTalking/Wav2Lip baseline.

## Phase 1 deferral

MuseTalk is not part of the Phase 1 Android idle-video voice FAQ MVP. Re-open only after the MVP is accepted and a GPU-backed digital-human enhancement phase is approved.

## Preconditions

- Wav2Lip pilot baseline and device acceptance exist
- Suitable GPU and MuseTalk assets are available

## Scope and allowed changes

- `Separate integration/config/evidence only`
- `docs/evidence/TASK-016/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Replacing baseline without evidence

## Detailed execution

1. Create a separate branch/environment; do not disturb the accepted Wav2Lip baseline.
2. Install MuseTalk according to current upstream requirements and record exact versions/assets.
3. Run the same script, avatar, audio and network test profile used for Wav2Lip.
4. Compare VRAM, FPS, first-frame/first-audio latency, visual quality and stability.
5. Recommend adopt/defer/reject with rollback and cost impact.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
nvidia-smi
```
```powershell
python -m pytest tests/livetalking -q
```

## Required deliverables

- [ ] Comparable benchmark evidence
- [ ] Adopt/defer/reject decision
- [ ] No baseline regression

## Acceptance criteria

- [ ] Separate environment/branch
- [ ] Quality/latency/VRAM comparison
- [ ] Rollback and recommendation

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
