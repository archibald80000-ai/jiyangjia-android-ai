# GitHub workflow

## Repository

Target public repository: `archibald80000-ai/jiyangjia-ai-kiosk`.

## Branching

- `main`: protected, reviewed and expected to remain coherent.
- `task/TASK-###-slug`: one task.
- `fix/...`: narrow urgent corrections.
- `upstream/livetalking-YYYYMMDD`: explicit upstream evaluation.

## Labels to create

- `area:android`, `area:gateway`, `area:livetalking`, `area:audio`, `area:knowledge`, `area:deploy`, `area:docs`
- `type:task`, `type:bug`, `type:risk`, `type:decision`
- `priority:p0`, `priority:p1`, `priority:p2`
- `status:blocked`, `status:needs-device`, `status:needs-gpu`, `status:needs-owner`

## PR expectations

PR title begins with task number. Body lists scope, actual tests, files, risks, secrets check, upstream impact and rollback. Draft by default until acceptance evidence exists.

## Publication

Use `scripts/publish_public_repo.ps1` from an authenticated Windows environment. It validates that the target is public and refuses to publish when tracked secret files are detected.
