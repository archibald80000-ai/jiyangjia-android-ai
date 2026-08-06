# Deployment

TASK-014 deploys only the lightweight FastAPI Gateway on the CPU-only Tencent Cloud host. It does not run LiveTalking, Wav2Lip, MuseTalk, local LLMs or GPU inference.

Server secrets must be supplied through an untracked `.env.local` placed beside this repository root. Do not commit it and do not print values in logs.

Minimal runtime directories:

```bash
mkdir -p gateway/logs var/knowledge
chmod 700 var/knowledge
```

Start from the repository root:

```bash
cd deploy
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1/api/v1/health
```

The Compose file mounts:

- `gateway/app` read-only into the container;
- `gateway/logs` for runtime logs;
- `var/knowledge` for SQLite and FAISS persistence;
- `.env.local` as service environment.

Production completion still requires domain/TLS, device auth, firewall/security group verification, resource measurements, backup and rollback evidence.
