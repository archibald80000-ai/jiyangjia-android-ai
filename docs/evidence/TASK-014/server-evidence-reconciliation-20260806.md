# TASK-014 Server Evidence Reconciliation

Date: 2026-08-06

Source: user-provided report from the server-management conversation thread. This file records sanitized deployment evidence only. No passwords, API keys, cookies, `.env.local` values, raw recordings or source business materials are included.

## Conclusion

TASK-014 is `PARTIAL`.

The Tencent Cloud host is reachable and currently runs a Docker Compose + Nginx mock Gateway that answers health checks and one text dialogue endpoint. It is not aligned with the current local TASK-013 commit `b67dbf09cfbed6ed6cd6a137c046c4138ac9d3aa`, does not contain the brand transcript normalization module, and does not expose the full MVP API contract required for Android acceptance.

Do not proceed to `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md` until TASK-014 is redeployed or reconciled against the current Gateway code and all required endpoints are verified.

## Server

- Cloud vendor: Tencent Cloud.
- Public endpoint: `120.53.86.89` by IP only; no domain is bound.
- OS: `Ubuntu 24.04.4 LTS`.
- CPU: AMD EPYC 7K62 host class, current allocation observed as 2 cores.
- Memory: `1.9Gi` observed.
- Disk: 50G total, about 8.2G used, about 39G available.
- GPU: none; only `Cirrus Logic GD 5446` virtual display controller observed.
- Host firewall: `ufw` active with `22/tcp`, `80/tcp`, `443/tcp`.
- Cloud security group: not verified from cloud console in the server thread.

## Deployment Shape

- Deployment directory: `/opt/jiyangjia-ai`.
- Existing backup: `/opt/jiyangjia-ai/backups/task014-20260806-034843`.
- Git metadata on server: missing; `/opt/jiyangjia-ai` is not a Git repository.
- Current branch/commit on server: missing.
- Alignment with local TASK-013 brand-normalization commit `b67dbf09cfbed6ed6cd6a137c046c4138ac9d3aa`: no.
- Runtime: Docker Compose with service `jiyangjia-gateway`, `restart: unless-stopped`.
- Container Python: `Python 3.12.13`.
- Host Python: `Python 3.12.3`.
- Gateway command: `uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 1`.
- Reverse proxy: Nginx.
- TLS: not enabled; current tests use HTTP/IP.

## Environment Variables

Only configured/missing state was reported:

- Doubao ASR variables: `missing`.
- Doubao TTS variables: `missing`.
- Doubao/Ark LLM variables: `missing`.
- Embedding variables: `missing`.
- OpenAI-compatible fallback variables: `missing`.
- Gateway runtime variables: `APP_NAME=configured`, `APP_VERSION=configured`, `TZ=configured`.

This means real Provider deployment is not complete on the server.

## Endpoint Checks

Reported local server checks:

| Endpoint | Status | Result |
|---|---:|---|
| `GET /health` | 200 | reachable |
| `GET /api/v1/health` | 200 | reachable |
| `GET /api/v1/client/config` | 404 | missing |
| `GET /api/v1/knowledge/status` | 404 | missing |
| `POST /api/v1/dialogue/text` | 200 | mock text dialogue reachable, request_id returned |
| `POST /api/v1/dialogue/audio` | 404 | missing |
| `GET /api/v1/audio/{audio_id}` | not verified | no audio_id produced; sample probe returned 404 |

The current server implementation does not satisfy the MVP API contract required by `docs/api/MVP_API_SPEC.md`.

## Brand Normalization Check

- `gateway/app/transcript_normalization.py` on server: not present.
- `/api/v1/dialogue/audio` normalization branch: not present because the route is missing.
- `transcript.raw_text` preservation: not present in the current server response shape.

The server does not include the TASK-013 follow-up fix for ASR brand homophone normalization.

## Knowledge Data

- SQLite database path: not configured.
- FAISS index path: not configured.
- Imported FAQ count: not configured.
- `approved` / `draft` / `rejected` counts: not configured.
- Raw `E:\work\积养家` material scan/upload: not performed according to the server thread report.

## Logs And Rollback

Reported log/evidence locations on server:

- Bootstrap log: `/opt/jiyangjia-ai/logs/server-bootstrap.log`.
- Gateway evidence log: `/opt/jiyangjia-ai/gateway/logs/task014_gateway_evidence_20260806-172520.log`.
- Gateway runtime logs: `/opt/jiyangjia-ai/gateway/logs` and `docker logs jiyangjia-gateway`.
- Nginx logs: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`.
- Process checks: `docker compose ps`, `docker ps`.

Suggested rollback from the server thread:

```bash
cd /opt/jiyangjia-ai/docker
docker compose down
cp -a /opt/jiyangjia-ai/backups/task014-20260806-034843/gateway /opt/jiyangjia-ai/gateway
docker compose up -d
```

`.env.local` backup state: not present; no `.env.local` was found on the server.

## Required Unblock Actions

1. Redeploy or rebuild `/opt/jiyangjia-ai` from the current project source, aligned to commit `b67dbf09cfbed6ed6cd6a137c046c4138ac9d3aa` or a later reviewed commit.
2. Preserve any existing backup and do not overwrite server secrets.
3. Configure real Provider environment variables on the server secret path without printing values.
4. Verify the full required API surface:
   - `GET /health`
   - `GET /api/v1/health`
   - `GET /api/v1/client/config`
   - `GET /api/v1/knowledge/status`
   - `POST /api/v1/knowledge/index`
   - `POST /api/v1/knowledge/search`
   - `POST /api/v1/dialogue/text`
   - `POST /api/v1/dialogue/audio`
   - `GET /api/v1/audio/{audio_id}`
5. Confirm `gateway/app/transcript_normalization.py` exists on the server and audio dialogue preserves `transcript.raw_text` while normalizing common `积养家` homophones.
6. Record process status, resource usage, firewall/security group status, logs, backup and rollback evidence.
