#!/usr/bin/env bash
set -euo pipefail

ROOT="${JIYANGJIA_ROOT:-/opt/jiyangjia-ai}"
RELEASE="${1:-$ROOT/releases/release-task015b-realtime-20260807T095914Z}"
ENV_FILE="$ROOT/secrets/.env.local"
COMPOSE_FILE="$RELEASE/deploy/docker-compose.yml"
KNOWLEDGE_DIR="$RELEASE/var/knowledge"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="$ROOT/backups/task014h-demo-online-$STAMP"

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "missing required file: $1" >&2
    exit 2
  fi
}

require_file "$ENV_FILE"
require_file "$COMPOSE_FILE"
require_file "$KNOWLEDGE_DIR/jiyangjia.db"
require_file "$KNOWLEDGE_DIR/faiss.index"

install -d -m 700 "$BACKUP_DIR"
install -m 600 "$ENV_FILE" "$BACKUP_DIR/secrets.env.local"
install -m 600 "$COMPOSE_FILE" "$BACKUP_DIR/docker-compose.yml"
install -m 600 /etc/nginx/conf.d/jiyangjia-ai.conf "$BACKUP_DIR/nginx.conf"
if [[ -f /etc/nginx/snippets/jiyangjia-gateway-locations.conf ]]; then
  install -m 600 /etc/nginx/snippets/jiyangjia-gateway-locations.conf "$BACKUP_DIR/nginx-locations.conf"
fi

python3 - "$KNOWLEDGE_DIR/jiyangjia.db" "$BACKUP_DIR/jiyangjia-v22.db" <<'PY'
import sqlite3
import sys

source = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
target = sqlite3.connect(sys.argv[2])
with target:
    source.backup(target)
source.close()
target.close()
PY
install -m 600 "$KNOWLEDGE_DIR/faiss.index" "$BACKUP_DIR/faiss-v22.index"

python3 - "$ENV_FILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
lines = path.read_text(encoding="utf-8").splitlines()
key = "JIYANGJIA_LLM_PROVIDER"
replacement = f"{key}=doubao"
updated = []
found = False
for line in lines:
    if line.strip().startswith(f"{key}="):
        updated.append(replacement)
        found = True
    else:
        updated.append(line)
if not found:
    updated.append(replacement)
path.write_text("\n".join(updated) + "\n", encoding="utf-8")
PY
chmod 600 "$ENV_FILE"

python3 - "$COMPOSE_FILE" "$ENV_FILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
env_file = sys.argv[2]
text = path.read_text(encoding="utf-8")
old = "      - ../secrets/.env.local"
new = f"      - {env_file}"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("compose env_file entry was not recognized")
path.write_text(text, encoding="utf-8")
PY

cd "$RELEASE/deploy"
docker compose up -d --no-deps --force-recreate gateway

for _ in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8080/api/v1/readiness >/tmp/task014h-readiness.json; then
    break
  fi
  sleep 2
done

python3 - /tmp/task014h-readiness.json <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
providers = data.get("providers", {})
safe = {
    "ready": data.get("ready"),
    "providers": {
        name: {
            "provider": item.get("provider"),
            "ready": item.get("ready"),
            "missing": item.get("missing"),
        }
        for name, item in providers.items()
    },
}
print(json.dumps(safe, ensure_ascii=False))
if not data.get("ready") or providers.get("llm", {}).get("provider") != "doubao":
    raise SystemExit(3)
PY

echo "backup_dir=$BACKUP_DIR"
echo "env_file=configured"
echo "env_mode=$(stat -c %a "$ENV_FILE")"
