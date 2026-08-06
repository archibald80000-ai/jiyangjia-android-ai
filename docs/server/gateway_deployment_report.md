# Gateway 部署报告（阶段二最小网关）

日期：2026-08-06

## 目标

- 在 `/opt/jiyangjia-ai` 上部署最小可运行 Gateway（Mock）
- 提供 `GET /health`
- 提供 `GET /api/v1/health`
- 提供 `POST /api/v1/dialogue/text`
- 通过 Nginx 反向代理到 `http://120.53.86.89/`
- 检查服务重启后自恢复与资源占用

## 已完成项

- 已同步网关源代码到 `/opt/jiyangjia-ai/gateway`
- 已同步 `deploy/docker-compose.yml` 到 `/opt/jiyangjia-ai/docker/docker-compose.yml`
- 已同步 Nginx 配置到 `/etc/nginx/sites-available/jiyangjia-gateway`
- 已启用默认站点反代（`/health` 与 `/api/`）
- 已通过 `docker compose up -d` 拉起服务并设置 `restart: unless-stopped`
- `POST /api/v1/dialogue/text` 仅返回 mock 回答（未接真实 Provider）

## 已安装/更新的软件与系统配置

- `swap`: 已设置 2.0 GiB `/swap.img`，并写入 `/etc/fstab`
- `fail2ban`: 安装并启用，`sshd` jail 已配置
- `UFW`: 已启用，入站允许 `22/tcp`, `80/tcp`, `443/tcp`
- Docker 日志策略:
  - `/etc/docker/daemon.json` 中加入 `log-driver=json-file` 与 `max-size=10m max-file=5`
- 时区: `Asia/Shanghai`

## 真实验证（命令及结果）

### 1) 容器状态

```bash
cd /opt/jiyangjia-ai/docker
docker compose ps
```

结果：

- `jiyangjia-gateway`：`Up ... (healthy)`
- 端口映射：`0.0.0.0:8080->8080/tcp`

### 2) 健康检查

```bash
curl http://127.0.0.1/health
curl http://120.53.86.89/health
curl http://127.0.0.1/api/v1/health
```

结果：三者均返回 `{"ok":true,...}`。

### 3) 对话接口（Mock）

```bash
cat >/tmp/dialogue.json <<'EOF'
{"text":"hello","session_id":"sess-test"}
EOF
curl -X POST http://127.0.0.1/api/v1/dialogue/text \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/dialogue.json
```

结果：

返回包含 `request_id/session_id/answer.text/knowledge.status=mock` 的 JSON。

### 4) 重启恢复验证

1. `sudo reboot`
2. 重启后执行同样 `docker compose ps`、`curl 127.0.0.1/health`、`curl /api/v1/dialogue/text`。

结果：

- 重启后服务仍为 `Up ... (healthy)`，可正常返回健康接口与 mock 对话响应。

### 5) 资源与安全命令

```bash
free -h
docker stats --no-stream
ufw status
fail2ban-client status
```

结果：

- `free -h`: 内存 1.9Gi，Swap 2.0Gi 可用
- `docker stats --no-stream`: Gateway 内存约 30-60MiB（运行时变化）
- `ufw status`: active，22/80/443 入站允许
- `fail2ban-client status`: jail `sshd` 已启用

## 未安装项（本阶段真实原因）

- HTTPS/TLS（未配域名）
- 豆包真实调用（按要求 Mock 阶段）
- Android APK 构建与部署（服务器阶段未执行）

## 下一步建议

- 按 `docs/server/security_baseline.md` 完成下一阶段的最小加固（如 Nginx 证书/鉴权）
- 在 Android 端接入后再切到真实 Provider 并保留 mock 兼容字段
