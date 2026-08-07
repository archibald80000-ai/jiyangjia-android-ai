# Deployment

TASK-014 deploys only the lightweight FastAPI Gateway on the CPU-only Tencent Cloud host. It does not run LiveTalking, Wav2Lip, MuseTalk, local LLMs or GPU inference.

Server secrets must be supplied through an untracked `secrets/.env.local` beside the deployment root. Do not commit it and do not print values in logs.

Minimal runtime directories:

```bash
mkdir -p gateway/logs var/knowledge
mkdir -p secrets
chmod 700 var/knowledge
chmod 700 secrets
[ -f secrets/.env.local ] && chmod 600 secrets/.env.local
```

Production origin: `https://ai-jiyangjia.cloud`. Install the Nginx virtual-host and shared location files as documented in `docs/server/DEPLOY.md`.

Start from the repository root:

```bash
cd deploy
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8080/api/v1/health
```

The Compose file mounts:

- `gateway/app` read-only into the container;
- `gateway/logs` for runtime logs;
- `var/knowledge` for SQLite and FAISS persistence;
- `secrets/.env.local` as service environment.

Port 8080 is loopback-only. Public access must use Nginx on 443. Production completion remains blocked until Tencent ICP/domain access onboarding releases the current DNSPod webblock and external TLS plus Certbot dry-run pass.
