# TASK-003: Run the first Wav2Lip WebRTC/WHEP baseline

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-002
- **Branch:** `task/TASK-003-wav2lip-webrtc-baseline`
- **Owner:** Codex / assigned developer

## Objective

Run the first Wav2Lip WebRTC/WHEP baseline.

## Preconditions

- TASK-002 is DONE or PARTIAL with a usable runtime
- Wav2Lip model and Avatar requirements are understood

## Scope and allowed changes

- `Local ignored model/avatar directories`
- `scripts/start_livetalking.ps1`
- `docs/evidence/TASK-003/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- MuseTalk
- Multi-concurrency
- Production deployment

## Detailed execution

1. Check required model and Avatar files by exact path and non-zero size; record source and checksum when available.
2. If assets are missing, stop before fake startup and produce exact manual download/placement instructions.
3. Launch LiveTalking with Wav2Lip and WebRTC/WHEP using the locked checkout; capture full sanitized startup log and PID/stop procedure.
4. Open the official page and establish one stream. Record browser/client, session ID format, audio/video outcome and network ports.
5. Capture `inferfps`/`finalfps` only from real logs and run a minimum stability interval appropriate to the environment.
6. Do not start MuseTalk or alter core upstream code.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
Get-ChildItem third_party/LiveTalking/models -ErrorAction SilentlyContinue
```
```powershell
Get-ChildItem third_party/LiveTalking/data/avatars -ErrorAction SilentlyContinue
```
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_livetalking.ps1
```
```powershell
Invoke-WebRequest http://127.0.0.1:8010/index.html -UseBasicParsing
```

## Required deliverables

- [ ] scripts/start_livetalking.ps1
- [ ] docs/evidence/TASK-003/wav2lip-baseline.md
- [ ] Startup/stream logs or exact BLOCKED evidence

## Acceptance criteria

- [ ] Required weights/avatar locations verified
- [ ] Service starts or exact blocker is captured
- [ ] Web page and WHEP/WebRTC result recorded
- [ ] Real FPS only reported from logs

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
