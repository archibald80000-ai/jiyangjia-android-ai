# TASK-014 Server Redeployment Request

Date: 2026-08-06

Purpose: hand this to the server-management thread so Tencent Cloud is redeployed from the current Gateway code and verified before Android real-device acceptance.

Do not print passwords, API keys, tokens, cookies, `.env.local` values, raw recordings or private business data. Only report `configured` / `missing` for secrets.

## Target

- Repository: `https://github.com/archibald80000-ai/jiyangjia-android-ai.git`
- Required source branch: `task/TASK-014-tencent-gateway-deployment`.
- Required source commit: use the latest reviewed commit on that branch, not the old mock deployment.
- Server: Tencent Cloud `120.53.86.89`
- Server target directory: `/opt/jiyangjia-ai`
- Runtime: Docker Compose + Nginx
- Gateway port: container `8080`, proxied through Nginx `/health` and `/api/`

## Required Server State

The server must contain the current Gateway code, including:

- `gateway/app/transcript_normalization.py`
- `GET /api/v1/client/config`
- `POST /api/v1/knowledge/index`
- `POST /api/v1/knowledge/search`
- `GET /api/v1/knowledge/status`
- `POST /api/v1/dialogue/audio`
- `GET /api/v1/audio/{audio_id}`

## Safe Redeploy Steps

Run on the server. Adjust only paths if your existing deployment uses a different root.

```bash
set -euo pipefail
TASK_TS="$(date +%Y%m%d-%H%M%S)"
sudo mkdir -p /opt/jiyangjia-ai/backups /opt/jiyangjia-ai/releases /opt/jiyangjia-ai/secrets
sudo chmod 700 /opt/jiyangjia-ai/secrets

# Backup the current deployment without recursing into previous backups.
sudo tar --exclude='/opt/jiyangjia-ai/backups' \
  -czf "/opt/jiyangjia-ai/backups/pre-current-gateway-${TASK_TS}.tgz" \
  -C /opt jiyangjia-ai

# Fetch current source into a fresh release directory.
sudo git clone https://github.com/archibald80000-ai/jiyangjia-android-ai.git \
  "/opt/jiyangjia-ai/releases/release-${TASK_TS}"
cd "/opt/jiyangjia-ai/releases/release-${TASK_TS}"
sudo git fetch origin task/TASK-014-tencent-gateway-deployment
sudo git checkout origin/task/TASK-014-tencent-gateway-deployment

git rev-parse HEAD
git status --short

# Prepare runtime directories.
sudo mkdir -p gateway/logs var/knowledge
sudo chmod 700 var/knowledge
```

## Secret Placement

Create or copy `/opt/jiyangjia-ai/secrets/.env.local` using the authorized secret source. Do not print it. This is the only env file path the Compose service should read.

Minimum provider selection expected for real MVP:

```bash
JIYANGJIA_ASR_PROVIDER=doubao
JIYANGJIA_TTS_PROVIDER=doubao
JIYANGJIA_LLM_PROVIDER=doubao
JIYANGJIA_EMBEDDING_PROVIDER=doubao
KNOWLEDGE_PROVIDER=sqlite_faiss_lightweight_rag
JIYANGJIA_KNOWLEDGE_DB_PATH=/app/var/knowledge/jiyangjia.db
JIYANGJIA_KNOWLEDGE_FAISS_PATH=/app/var/knowledge/faiss.index
```

The actual `.env.local` must also include the authorized Doubao ASR/TTS, Ark/Doubao LLM and Embedding credentials and model names. Output only configured/missing status.

Check the secret file path and permissions without printing values:

```bash
test -f /opt/jiyangjia-ai/secrets/.env.local
sudo chmod 600 /opt/jiyangjia-ai/secrets/.env.local
sudo stat -c '%a %U %G %n' /opt/jiyangjia-ai/secrets/.env.local
python3 scripts/check_provider_env.py \
  --env-file /opt/jiyangjia-ai/secrets/.env.local \
  --compose-file deploy/docker-compose.yml \
  --require-real-mvp \
  > /tmp/task014_provider_env_preflight.json
cat /tmp/task014_provider_env_preflight.json
```

If this command exits non-zero or `real_mvp_ready` is false, stop and fix `/opt/jiyangjia-ai/secrets/.env.local`. Do not rebuild or retest dialogue until this preflight passes.

## Start Gateway

```bash
cd "/opt/jiyangjia-ai/releases/release-${TASK_TS}/deploy"
sudo docker compose down || true
sudo docker compose up -d --build
sudo docker compose ps
sudo docker stats --no-stream
```

If the old deployment uses a different Compose project, stop only the old `jiyangjia-gateway` container after the backup is complete.

## Nginx

Confirm Nginx forwards both `/health` and `/api/` to `127.0.0.1:8080`.

```bash
sudo nginx -t
sudo systemctl reload nginx
curl -fsS http://127.0.0.1/api/v1/health
curl -sS http://127.0.0.1/api/v1/readiness -o /tmp/task014_readiness.json -w '%{http_code}\n'
curl -fsS http://120.53.86.89/api/v1/health
```

TLS/domain remains incomplete until a domain and certificate are configured. If still IP-only HTTP, keep TASK-014 as `PARTIAL`.

## Knowledge Index Smoke

Build a sanitized index payload from the approved demo FAQ only. Do not scan or upload `E:\work\积养家`.

```bash
cd "/opt/jiyangjia-ai/releases/release-${TASK_TS}"
python3 - <<'PY'
import json
from pathlib import Path

src = json.loads(Path("knowledge-test/faq_mvp_approved.example.json").read_text(encoding="utf-8"))
docs = []
for item in src["documents"]:
    text = "\n".join([
        f"标题：{item['title']}",
        "问题：" + "；".join(item.get("questions", [])),
        "回答：" + item["answer"],
    ])
    docs.append({
        "id": item["id"],
        "title": item["title"],
        "text": text,
        "status": item["status"],
        "source_uri": item.get("source_uri"),
    })
Path("/tmp/task014_knowledge_index.json").write_text(
    json.dumps({"documents": docs}, ensure_ascii=False),
    encoding="utf-8",
)
print(json.dumps({"documents": len(docs)}, ensure_ascii=False))
PY

curl -sS -X POST \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/task014_knowledge_index.json \
  -o /tmp/task014_knowledge_index_result.json \
  -w '%{http_code}\n' \
  http://127.0.0.1/api/v1/knowledge/index

curl -sS http://127.0.0.1/api/v1/knowledge/status \
  -o /tmp/task014_knowledge_status.json \
  -w '%{http_code}\n'

curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d '{"query":"积养家是做什么的","top_k":3,"request_id":"task014-search"}' \
  -o /tmp/task014_knowledge_search.json \
  -w '%{http_code}\n' \
  http://127.0.0.1/api/v1/knowledge/search
```

## Dialogue/Text Smoke

Before calling dialogue endpoints, inspect readiness once. If it reports missing credentials, stop and fix `/opt/jiyangjia-ai/secrets/.env.local`; do not keep retesting upload/dialogue.

```bash
curl -sS http://127.0.0.1/api/v1/readiness \
  -o /tmp/task014_readiness.json \
  -w '%{http_code}\n'
python3 - <<'PY'
import json
p=json.load(open('/tmp/task014_readiness.json', encoding='utf-8'))
print(json.dumps({
  "ready": p.get("ready"),
  "status": p.get("status"),
  "providers": {
    name: {"provider": info.get("provider"), "ready": info.get("ready"), "missing": info.get("missing")}
    for name, info in p.get("providers", {}).items()
  },
}, ensure_ascii=False))
PY
```

```bash
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-Request-Id: task014-dialogue-text' \
  -d '{"text":"积养家是做什么的？","session_id":"task014"}' \
  -o /tmp/task014_dialogue_text.json \
  -w '%{http_code}\n' \
  http://127.0.0.1/api/v1/dialogue/text

python3 - <<'PY'
import json
p=json.load(open('/tmp/task014_dialogue_text.json', encoding='utf-8'))
print(json.dumps({
  "request_id": p.get("request_id"),
  "sources": len(p.get("sources", [])),
  "audio_id": p.get("tts", {}).get("audio_id"),
  "answer_chars": len(p.get("answer", {}).get("text", "")),
}, ensure_ascii=False))
PY
```

Fetch the generated audio:

```bash
AUDIO_ID="$(python3 - <<'PY'
import json
p=json.load(open('/tmp/task014_dialogue_text.json', encoding='utf-8'))
print(p.get('tts', {}).get('audio_id', ''))
PY
)"
test -n "$AUDIO_ID"
curl -sS -o /tmp/task014_answer_audio.bin \
  -w '%{http_code} %{content_type} %{size_download}\n' \
  "http://127.0.0.1/api/v1/audio/${AUDIO_ID}"
```

## Dialogue/Audio Smoke

Prefer a non-sensitive speech sample. If none exists, generate one with the configured TTS provider and feed it to ASR:

```bash
cd "/opt/jiyangjia-ai/releases/release-${TASK_TS}"
python3 -m venv /tmp/jiyangjia-task014-smoke
. /tmp/jiyangjia-task014-smoke/bin/activate
pip install --no-cache-dir -r gateway/requirements.txt
python scripts/test_tts_provider.py \
  --provider doubao \
  --env-file .env.local \
  --text "请问季养家可以咨询什么" \
  --output /tmp/task014_question.mp3

curl -sS -X POST \
  -H 'X-Request-Id: task014-dialogue-audio' \
  -F 'session_id=task014-audio' \
  -F 'duration_ms=2500' \
  -F 'sample_rate=24000' \
  -F 'input_device=server-smoke' \
  -F 'audio=@/tmp/task014_question.mp3;type=audio/mpeg' \
  -o /tmp/task014_dialogue_audio.json \
  -w '%{http_code}\n' \
  http://127.0.0.1/api/v1/dialogue/audio

python3 - <<'PY'
import json
p=json.load(open('/tmp/task014_dialogue_audio.json', encoding='utf-8'))
print(json.dumps({
  "request_id": p.get("request_id"),
  "raw_text": p.get("transcript", {}).get("raw_text"),
  "text": p.get("transcript", {}).get("text"),
  "normalization": p.get("transcript", {}).get("normalization"),
  "sources": len(p.get("sources", [])),
  "audio_id": p.get("tts", {}).get("audio_id"),
}, ensure_ascii=False))
PY
```

Expected: if ASR outputs a common `ji/yang/jia` homophone, `transcript.text` is normalized to `积养家`, and `transcript.raw_text` preserves the original provider text.

## Required Evidence To Return

Return these items to the main project thread:

1. Server OS/CPU/memory/disk/GPU check.
2. Backup archive path and size.
3. Deployment directory, branch and exact commit SHA.
4. Docker Compose file path, `docker compose ps` and `docker stats --no-stream`.
5. Nginx config path, `nginx -t`, HTTP/TLS status and open ports.
6. Secret status only as configured/missing.
   - Include `/tmp/task014_provider_env_preflight.json`.
7. Endpoint results for all required MVP APIs.
8. Knowledge status counts and source count from search.
9. Dialogue/text result with request_id, sources, audio_id and audio fetch status.
10. Dialogue/audio result with transcript text/raw_text/normalization, sources, audio_id and audio fetch status.
11. Log paths, rollback command and whether TASK-014 is `DONE`, `PARTIAL` or `BLOCKED`.

TASK-014 can be `DONE` only if the current code is deployed, the full API contract is reachable, provider credentials are configured without leakage, knowledge is indexed, audio dialogue works, logs/rollback/resource evidence exist, and either TLS/device auth are completed or explicitly accepted as pilot exceptions.
