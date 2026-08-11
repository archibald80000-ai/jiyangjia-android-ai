#!/usr/bin/env bash
set -euo pipefail

ROOT="${JIYANGJIA_ROOT:-/opt/jiyangjia-ai}"
RELEASE="${1:-$ROOT/releases/release-task015b-realtime-20260807T095914Z}"
PORT="${TASK014H_CANDIDATE_PORT:-18090}"
CONTAINER="jiyangjia-v21-candidate"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
CANDIDATE="$ROOT/candidates/task014h-v21-$STAMP"

test -f "$ROOT/secrets/.env.local"
test -d "$RELEASE/gateway/app"

if docker ps -a --format '{{.Names}}' | grep -Fxq "$CONTAINER"; then
  docker rm -f "$CONTAINER" >/dev/null
fi

install -d -m 700 \
  "$CANDIDATE/knowledge" \
  "$CANDIDATE/admin" \
  "$CANDIDATE/assets" \
  "$CANDIDATE/logs"

docker run -d \
  --name "$CONTAINER" \
  --restart no \
  --env-file "$ROOT/secrets/.env.local" \
  -e JIYANGJIA_ASR_PROVIDER=doubao \
  -e JIYANGJIA_TTS_PROVIDER=doubao \
  -e JIYANGJIA_LLM_PROVIDER=doubao \
  -e JIYANGJIA_EMBEDDING_PROVIDER=doubao \
  -e JIYANGJIA_KNOWLEDGE_DB_PATH=/app/var/knowledge/jiyangjia.db \
  -e JIYANGJIA_KNOWLEDGE_FAISS_PATH=/app/var/knowledge/faiss.index \
  -e JIYANGJIA_ADMIN_DB_PATH=/app/var/admin/admin.db \
  -e JIYANGJIA_ADMIN_UPLOAD_DIR=/app/var/knowledge/uploads \
  -e JIYANGJIA_ASSET_DIR=/app/var/assets \
  -p "127.0.0.1:$PORT:8080" \
  -v "$RELEASE/gateway/app:/app/app:ro" \
  -v "$CANDIDATE/knowledge:/app/var/knowledge" \
  -v "$CANDIDATE/admin:/app/var/admin" \
  -v "$CANDIDATE/assets:/app/var/assets" \
  -v "$CANDIDATE/logs:/app/logs" \
  deploy-gateway >/dev/null

for _ in $(seq 1 45); do
  if curl -fsS "http://127.0.0.1:$PORT/api/v1/readiness" >/tmp/task014h-v21-readiness.json; then
    break
  fi
  sleep 2
done

python3 - /tmp/task014h-v21-readiness.json <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
providers = data.get("providers", {})
if not data.get("ready"):
    raise SystemExit("candidate readiness is false")
if any(providers.get(name, {}).get("provider") != "doubao" for name in ("asr", "tts", "llm", "embedding")):
    raise SystemExit("candidate is not using all required real providers")
print("providers=ready")
PY

echo "candidate_dir=$CANDIDATE"
echo "container=$CONTAINER"
echo "port=$PORT"
