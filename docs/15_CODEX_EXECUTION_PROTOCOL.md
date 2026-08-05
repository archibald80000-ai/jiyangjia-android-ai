# Codex execution protocol

## Session start

Codex must state:

1. current directory and branch;
2. current task and dependencies;
3. existing changed files;
4. environment/tool availability relevant to the task;
5. exact files it plans to modify;
6. tests it will run;
7. risks and stop conditions.

Then execute the task without waiting for routine confirmation, unless a destructive/sensitive operation is required.

## During work

- Share concrete findings early.
- Do not repeatedly retry the same unexplained failure.
- Prefer minimal reversible changes.
- Keep logs under a task-specific evidence folder that is safe to commit or summarize.
- Preserve user files and unrelated local changes.

## Task close

Codex must report:

- completion status (`DONE`, `PARTIAL`, `BLOCKED`);
- changed files;
- exact commands and results;
- artifacts/paths;
- known gaps;
- risks introduced;
- rollback;
- updated memory/state;
- recommended next task.

## Prompt template

Use `.codex/TASK_EXECUTION_PROMPT.md` and replace the task number. The task file is authoritative if prompt text conflicts with it.
