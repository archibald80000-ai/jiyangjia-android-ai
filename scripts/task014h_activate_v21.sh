#!/usr/bin/env bash
set -euo pipefail

CANDIDATE="${1:?candidate directory is required}"
BACKUP_DIR="${2:?backup directory is required}"
ROOT="${JIYANGJIA_ROOT:-/opt/jiyangjia-ai}"
RELEASE="${3:-$ROOT/releases/release-task015b-realtime-20260807T095914Z}"
ACTIVE="$RELEASE/var/knowledge"
COMPOSE_DIR="$RELEASE/deploy"
TMP_DB="$ACTIVE/.task014h-v21.db.tmp"
TMP_FAISS="$ACTIVE/.task014h-v21.faiss.tmp"

for file in \
  "$CANDIDATE/knowledge/jiyangjia.db" \
  "$CANDIDATE/knowledge/faiss.index" \
  "$BACKUP_DIR/jiyangjia-v22.db" \
  "$BACKUP_DIR/faiss-v22.index"; do
  test -f "$file"
done

rollback() {
  set +e
  install -m 600 "$BACKUP_DIR/jiyangjia-v22.db" "$ACTIVE/.task014h-rollback.db.tmp"
  install -m 600 "$BACKUP_DIR/faiss-v22.index" "$ACTIVE/.task014h-rollback.faiss.tmp"
  mv -f "$ACTIVE/.task014h-rollback.db.tmp" "$ACTIVE/jiyangjia.db"
  mv -f "$ACTIVE/.task014h-rollback.faiss.tmp" "$ACTIVE/faiss.index"
  cd "$COMPOSE_DIR"
  docker compose up -d --no-deps --force-recreate gateway
  echo "rollback=restored_v22" >&2
}
trap rollback ERR

docker stop jiyangjia-v21-candidate >/dev/null

python3 - "$CANDIDATE/knowledge/jiyangjia.db" "$TMP_DB" <<'PY'
import sqlite3
import sys

source = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
if source.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
    raise SystemExit("candidate SQLite integrity check failed")
target = sqlite3.connect(sys.argv[2])
with target:
    source.backup(target)
source.close()
target.close()
PY
install -m 600 "$CANDIDATE/knowledge/faiss.index" "$TMP_FAISS"

cd "$COMPOSE_DIR"
docker compose stop gateway
mv -f "$TMP_DB" "$ACTIVE/jiyangjia.db"
mv -f "$TMP_FAISS" "$ACTIVE/faiss.index"
docker compose up -d --no-deps --force-recreate gateway

for _ in $(seq 1 45); do
  if curl -fsS http://127.0.0.1:8080/api/v1/knowledge/status >/tmp/task014h-v21-production-status.json; then
    break
  fi
  sleep 2
done

python3 - /tmp/task014h-v21-production-status.json <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
expected = {"approved": 41, "draft": 24, "rejected": 0}
vectors = data.get("vector_index", {})
if data.get("documents") != expected:
    raise SystemExit(f"unexpected document status: {data.get('documents')}")
if not vectors.get("ready") or vectors.get("vectors") != 65 or vectors.get("dimensions") != 2048:
    raise SystemExit(f"unexpected vector status: {vectors}")
print(json.dumps({"documents": data["documents"], "vector_index": vectors}, ensure_ascii=False))
PY

trap - ERR
docker rm jiyangjia-v21-candidate >/dev/null
echo "activation=success"
echo "rollback_dir=$BACKUP_DIR"
