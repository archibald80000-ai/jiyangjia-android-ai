# TASK-021A Public Resource Access Gate Evidence

## Result

`DONE / PRODUCTION_PUBLISHED`

The public resource gate and the grounded-response persona are deployed together. No real dialogue, ASR, LLM or TTS request was made during gate acceptance.

## Source and integration

- Gate branch: `codex/TASK-021-public-resource-gate`
- Gate implementation commit: `cb174c8`
- Persona source commit: `afe9c113f440fddc87e8365662648c01c70279a9`
- Integrated deployment commit: `9f2ce2780d002b49cc2b843e02b8fb85ac3fa644`
- Git remote: `https://github.com/archibald80000-ai/jiyangjia-android-ai.git`
- Plaintext password in repository/client/logs: no

## Saved state before integration

- Server snapshot: `/opt/jiyangjia-ai/backups/task021-reconcile-20260812T161020Z`
- Local repository bundle and working-tree snapshot: `E:\work\ai-kefu\backups\task021-reconcile-20260812T161019Z`
- Pre-deployment backup: `/opt/jiyangjia-ai/backups/task021-integrated-20260812T161522Z`
- Previous release: `/opt/jiyangjia-ai/releases/release-task021-persona-20260812T155015Z`
- Active integrated release: `/opt/jiyangjia-ai/releases/release-task021-integrated-20260812T161522Z`
- Secrets backup: yes, server-side only with restricted permissions

## Configuration status

- `JIYANGJIA_PUBLIC_GATE_PASSWORD_HASH`: configured
- `JIYANGJIA_PUBLIC_GATE_SESSION_SECRET`: configured
- `JIYANGJIA_PUBLIC_GATE_SESSION_TTL_SECONDS`: configured
- Secrets file mode: `600`
- Compose env-file path: `/opt/jiyangjia-ai/secrets/.env.local`
- Compose env-file format: `raw`

## Automated and browser verification

- Gateway/admin/knowledge/LLM tests: `99 passed`, one third-party FAISS/NumPy deprecation warning.
- Desktop public page: gate dialog, keyboard focus and invalid-password error visible.
- Mobile 390x844: gate displayed as a bottom panel.
- `/demo/kiosk`: virtual-human stage and consultation controls present; public navigation/gate absent.
- `localStorage`/`sessionStorage`: absent from the gate implementation.

## External HTTPS verification

| Check | Result |
| --- | --- |
| `GET /health` | `200` |
| `GET /api/v1/health` | `200` |
| `GET /api/v1/readiness` | `200` |
| `GET /` | `200`, protected navigation present |
| Unauthenticated knowledge redirect | `401` |
| `POST /api/v1/public-access/login` | `200` |
| Cookie `HttpOnly` | true |
| Cookie `Secure` | true |
| Cookie `SameSite=Strict` | true |
| Cookie `Max-Age=86400` | true |
| Authenticated session | `200`, authenticated true, `Cache-Control: no-store` |
| Knowledge-center redirect | `302`, allowlisted target |
| Public-materials redirect | `302`, allowlisted target |
| Logout | `200` |
| Redirect after logout | `401` |

## Production state

- `jiyangjia-gateway`: healthy, bound to `127.0.0.1:8080`.
- Container sample: `0.14%` CPU, `75.83 MiB / 1.922 GiB` memory (`3.85%`).
- Host memory: `1.9 GiB` total, about `1.3 GiB` available.
- Swap: `2.0 GiB` total, `48 MiB` used.
- Disk: `50 GiB` total, `13 GiB` used, `35 GiB` available (`27%`).
- Nginx configuration: valid and active; one `/access/` proxy location present.
- UFW: active; `22`, `80` and `443` allowed.
- Fail2ban: active with the `sshd` jail.

## Failure and recovery record

The first integrated release attempt stopped before switching because the non-root shell could not redirect Compose evidence into a root-only backup directory. The rollback completed to the prior persona release. The corrected attempt wrote temporary logs first and installed them with root permissions; it then deployed successfully. No Provider call was repeated.

## Rollback

1. Restore `/etc/nginx/snippets/jiyangjia-gateway-locations.conf` from `/opt/jiyangjia-ai/backups/task021-integrated-20260812T161522Z`.
2. Atomically point `/opt/jiyangjia-ai/current` to `/opt/jiyangjia-ai/releases/release-task021-persona-20260812T155015Z`.
3. Run `sudo docker compose -f deploy/docker-compose.yml up -d --build --force-recreate` from that release.
4. Run `sudo nginx -t` and reload Nginx only if the test succeeds.
