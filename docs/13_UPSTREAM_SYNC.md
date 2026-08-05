# Upstream synchronization

## Policy

LiveTalking is locked in `config/upstream-lock.json`. Updating it is a dedicated task, never an incidental dependency upgrade.

## Update procedure

1. Record current lock and local patches.
2. Fetch upstream without modifying the working branch.
3. Review release notes, commits, APIs, licenses and model requirements.
4. Create an upstream-update branch.
5. Update lock.
6. Re-run all LiveTalking API contract tests and Android integration smoke tests.
7. Document behavior and performance changes.
8. Merge only with rollback instructions.

## Patch ledger

Store unavoidable patches under `integration/livetalking_patches/` with:

- upstream commit;
- reason;
- changed behavior;
- application command;
- test evidence;
- removal condition.
