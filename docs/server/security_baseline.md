# 安全基线（TASK-014 当前状态）

## 基础安全
- `ufw`：active，入站默认拒绝
- 放行端口：`22/tcp`, `80/tcp`, `443/tcp`

## 登录防护
- `fail2ban` active
- Jail：`sshd`

## 时区与时间
- Timezone：`Asia/Shanghai`
- `timedatectl`：`System clock synchronized: yes`
- `ntp` 同步正常

## 运行时资源
- Swap：2.0Gi（`/swap.img`，`/etc/fstab` 持久化）
- 可见内存：1.9Gi（任务采样：`free -h`）

## 容器与日志
- Docker daemon：`/etc/docker/daemon.json`
  - `log-driver: json-file`
  - `log-opts.max-size: 10m`
  - `log-opts.max-file: 5`
- `deploy/docker-compose.yml` 容器日志：`max-size: 10m`，`max-file: 5`

## 端口/服务暴露
- Nginx：`/etc/nginx/nginx.conf` 有效，`systemctl is-active nginx`=active
- 外部只开 80/443，网关对外通过 Nginx 反代 80

## 风险提醒
- `/api/v1/*` 当前未加鉴权
- 真实 Provider 凭据缺失导致对话接口 503
- 未启用 HTTPS（任务当前仅 IP + HTTP 验证）
