# TASK-014: Deploy the lightweight gateway to Tencent Cloud

- **Status:** PLANNED
- **Priority:** P1
- **Dependencies:** TASK-013
- **Branch:** `task/TASK-014-tencent-gateway-deployment`
- **Owner:** Codex / assigned developer

## Objective

Deploy the lightweight gateway to Tencent Cloud.

## Preconditions

- TASK-013 is DONE
- Server access is authorized and backed up

## Scope and allowed changes

- `deploy/`
- gateway deployment config
- `docs/evidence/TASK-014/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- GPU inference on the 4 GB server

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

- [ ] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [ ] Add evidence links/results to this task.
- [ ] Update `PROJECT_STATE.md`.
- [ ] Update `memory/CURRENT_STATE.md`.
- [ ] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [ ] Recommend exactly one next task.
