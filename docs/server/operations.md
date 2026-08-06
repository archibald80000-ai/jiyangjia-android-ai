# Server Operations（Gateway 阶段）

## 部署目录

- 代码/服务：`/opt/jiyangjia-ai/gateway`
- Compose：`/opt/jiyangjia-ai/docker/docker-compose.yml`
- 日志：`/opt/jiyangjia-ai/logs`
- 运行命令日志：`/opt/jiyangjia-ai/logs/server-bootstrap.log`

## 维护命令（真实）

```bash
cd /opt/jiyangjia-ai/docker
sudo docker compose ps
sudo docker compose up -d --build
sudo docker compose down
sudo docker compose logs --tail 80
```

```bash
cd /opt/jiyangjia-ai/docker
sudo docker restart jiyangjia-gateway
```

## 健康检查（运维日常）

```bash
curl http://127.0.0.1/health
curl http://120.53.86.89/health
curl http://127.0.0.1/api/v1/health
```

```bash
cat >/tmp/dialogue.json <<'EOF'
{"text":"hello","session_id":"ops-check"}
EOF
curl -X POST http://127.0.0.1/api/v1/dialogue/text \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/dialogue.json
```

## 重启与恢复

```bash
sudo reboot
```

恢复后执行：

```bash
cd /opt/jiyangjia-ai/docker
docker compose ps
curl http://127.0.0.1/health
curl http://120.53.86.89/health
```

## 备份建议

- 定期备份：
  - `/opt/jiyangjia-ai/docker/docker-compose.yml`
  - `/opt/jiyangjia-ai/docker/nginx-jiyangjia.conf`
  - `/opt/jiyangjia-ai/gateway/app/main.py`
  - `/opt/jiyangjia-ai/logs/server-bootstrap.log`
  - `docs/server/*.md`

## 回滚

- 回滚步骤：
 1. `cd /opt/jiyangjia-ai/docker && docker compose down`
 2. 恢复上一个 compose 配置
 3. `docker compose up -d`
