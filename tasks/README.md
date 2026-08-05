# Task execution system

Every task is a bounded contract for Codex.

## Status flow

`PLANNED → IN_PROGRESS → DONE`
or `IN_PROGRESS → PARTIAL/BLOCKED`.

## Required task close-out

- Update the task front matter/status.
- Add real evidence and commands.
- Update `PROJECT_STATE.md`.
- Update `memory/CURRENT_STATE.md` and `memory/HANDOFF.md`.
- Add/modify ADR and `memory/DECISIONS.md` for architecture changes.
- Keep Mock/real distinctions explicit.

## Branch

`task/TASK-###-slug`

## Evidence directory

Implementation tasks may create `docs/evidence/TASK-###/` for sanitized logs, screenshots, test summaries and checksums. Do not commit secrets, raw customer recordings or huge model logs.
