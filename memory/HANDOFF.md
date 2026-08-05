# Handoff

## Read first

- `AGENTS.md`
- `PROJECT_STATE.md`
- `tasks/TASK-000_PROJECT_BOOTSTRAP.md`

## Known external paths

```text
Project: E:\work\安卓大屏AI语音客服系统
Raw materials (read-only): E:\work\积养家
```

## Upstream lock

```text
Repository: https://github.com/lipku/LiveTalking.git
Commit: c963ad409c556918b7d23999bf87c47a7c05c932
```

## Safety note

A `.env.local` may exist on the user's machine. Only report whether required variable names are configured; never print values or commit the file.

## First command group

```powershell
Set-Location "E:\work\安卓大屏AI语音客服系统"
git status
powershell -ExecutionPolicy Bypass -File .\scripts\check_prerequisites.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1
```

Replace this handoff after each completed task with the actual branch, commit, commands, results, blockers and exact next task.
