# TASK-014: Deploy the lightweight gateway to Tencent Cloud

- **Status:** PARTIAL
- **Priority:** P1
- **Dependencies:** TASK-013
- **Branch:** `task/TASK-014-tencent-gateway-deployment`
- **Owner:** Codex / assigned developer

## Objective

Deploy the lightweight gateway to Tencent Cloud.

## Preconditions

- TASK-013 is PARTIAL with local/backend E2E complete and Android device verification deferred
- Server access is authorized and backed up

## Scope and allowed changes

- `deploy/`
- gateway deployment config
- `docs/evidence/TASK-014/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- GPU inference on the CPU-only Tencent Cloud server

## Detailed execution

1. Audit OS, ports, disk, memory and existing services before deployment.
2. Deploy only the lightweight gateway and required datastore/reverse proxy.
3. Configure TLS, device token, firewall/security group, process restart, log rotation and health monitoring.
4. Run low-concurrency load/resource tests and record memory/CPU/bandwidth.
5. Document backup, rollback and secret placement. Do not deploy GPU inference on this server.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
curl -fsS https://<domain>/api/v1/health
```
```powershell
docker compose ps
```
```powershell
docker stats --no-stream
```

## Required deliverables

- [ ] Reproducible deployment config
- [ ] Security/resource evidence
- [ ] Rollback/operations guide

## Acceptance criteria

- [ ] TLS/reverse proxy
- [ ] Device auth
- [ ] Firewall
- [ ] Resource measurements
- [ ] Backup/log rotation/rollback

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

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## Reconciliation evidence

- Result: `PARTIAL`
- Evidence: `docs/evidence/TASK-014/server-evidence-reconciliation-20260806.md`
- Server: Tencent Cloud IP-only test host `120.53.86.89`, Ubuntu `24.04.4 LTS`, observed allocation 2 CPU cores, `1.9Gi` memory, 50G disk, no GPU.
- Current server deployment: Docker Compose + Nginx mock Gateway under `/opt/jiyangjia-ai`, with backup at `/opt/jiyangjia-ai/backups/task014-20260806-034843`.
- Server code alignment: not aligned with local commit `b67dbf09cfbed6ed6cd6a137c046c4138ac9d3aa`; `/opt/jiyangjia-ai` has no Git metadata.
- Verified reachable on server thread: `GET /health` -> 200, `GET /api/v1/health` -> 200, `POST /api/v1/dialogue/text` -> 200 with request_id.
- Missing on server thread: `GET /api/v1/client/config`, `GET /api/v1/knowledge/status`, `POST /api/v1/dialogue/audio`, `GET /api/v1/audio/{audio_id}`.
- Missing on server thread: real Provider environment variables, SQLite/FAISS knowledge configuration and TASK-013 brand normalization module.

Next action: continue exactly one task, TASK-014 remediation/redeploy to the current Gateway code and verify the full MVP API before entering TASK-015.

## Redeployment package prepared

- Result: still `PARTIAL`; server execution is not yet re-verified.
- Deployment config updated: `deploy/docker-compose.yml` now loads untracked `../.env.local`, persists `var/knowledge` for SQLite/FAISS, and health-checks `/api/v1/health`.
- Server handoff/runbook: `docs/evidence/TASK-014/server-redeployment-request-20260806.md`.
- Local checks:
  - `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway tests\e2e -q` -> 9 passed.
  - Docker Compose YAML parse -> PASS.
  - `scripts\verify_repository.ps1` -> PASS.

Next action remains TASK-014 server-side redeploy and evidence return. Do not enter TASK-015 yet.
