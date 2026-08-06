# Gateway 运维操作

## 目录与服务
- 部署：`/opt/jiyangjia-ai`
- Compose 文件：`/opt/jiyangjia-ai/docker/docker-compose.yml`
- Gateway 源码：`/opt/jiyangjia-ai/gateway`
- 日志：`/opt/jiyangjia-ai/logs`, `/opt/jiyangjia-ai/logs/task014_evidence`, `docker logs jiyangjia-gateway`
- 备份：`/opt/jiyangjia-ai/backups`（如 `pre-task014-20260806-185559.tgz`）
- Provider 环境文件：`/opt/jiyangjia-ai/secrets/.env.local`（权限 `600`，只查 configured/missing，不输出值）

## 日常命令
```bash
cd /opt/jiyangjia-ai/docker

docker compose ps
docker compose up -d --build
docker compose down
docker logs --tail 120 jiyangjia-gateway

docker restart jiyangjia-gateway
```

## 检查命令（本任务验收）
```bash
curl -sS -o /tmp/health.json -w "%{http_code}" http://127.0.0.1/health
curl -sS -o /tmp/v1_health.json -w "%{http_code}" http://127.0.0.1/api/v1/health
curl -sS -o /tmp/readiness.json -w "%{http_code}" http://127.0.0.1/api/v1/readiness
curl -sS -o /tmp/client_config.json -w "%{http_code}" http://127.0.0.1/api/v1/client/config
curl -sS -o /tmp/knowledge_status.json -w "%{http_code}" http://127.0.0.1/api/v1/knowledge/status
curl -sS -o /tmp/knowledge_index.json -w "%{http_code}" -H "Content-Type: application/json" -d '{"source":"knowledge-test/faq_mvp_approved.example.json","source_type":"json","only_approved":true,"force_reindex":true}' http://127.0.0.1/api/v1/knowledge/index
curl -sS -o /tmp/knowledge_search.json -w "%{http_code}" -H "Content-Type: application/json" -d '{"query":"积养家", "top_k": 3}' http://127.0.0.1/api/v1/knowledge/search
curl -sS -o /tmp/dialogue_text.json -w "%{http_code}" -H "Content-Type: application/json" -d '{"text":"确认服务时间","session_id":"ops"}' http://127.0.0.1/api/v1/dialogue/text
```

## 重启恢复
```bash
docker restart jiyangjia-gateway
sleep 20
docker compose ps
curl -sS -o /tmp/health_after.json -w "%{http_code}" http://127.0.0.1/health
```

## 回滚
1. `cd /opt/jiyangjia-ai/docker`
2. `docker compose down`
3. 备份目录恢复（或切换 `releases/` 下已知版本）
4. `docker compose up -d`
