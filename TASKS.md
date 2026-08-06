# Task index

The canonical machine-readable index is [`tasks/index.yaml`](tasks/index.yaml). Human-readable instructions are in [`tasks/README.md`](tasks/README.md).

Current status:

- `TASK-000`: `DONE`; environment/repository audit passed and LiveTalking locked checkout exists under ignored `third_party/LiveTalking`.
- `TASK-001`: `DONE`; locked LiveTalking upstream source audited with endpoint, model/asset, network, extension and compliance notes.
- `TASK-002`: `DONE`; isolated LiveTalking runtime exists under ignored `.venv\livetalking-task002`, dependencies/imports/PyTorch CUDA smoke check passed.
- Next action is `TASK-003`; do not start later tasks concurrently.

Current order:

`TASK-000 → 001 → 002 → 003 → 004 → 005 → 006 → 007 → 008 → 009 → 010 → 011 → 012 → 013 → 014 → 015 → 016 → 017`

Do not execute multiple implementation tasks concurrently unless a later task explicitly permits parallel work.
