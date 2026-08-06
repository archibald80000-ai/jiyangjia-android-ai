# Security Baseline（Gateway 阶段）

## 当前基线

- 防火墙：
  - `ufw` 已启用
  - 入站默认拒绝 (`deny`)
  - 允许：`22/tcp`, `80/tcp`, `443/tcp`
  - 出站默认允许
- 登录防护：
  - `fail2ban` 已安装并服务运行
  - 已启用 jail：`sshd`
- 时区/时间：
  - `Asia/Shanghai`
  - NTP 同步为 `active` 且 `System clock synchronized: yes`
- 容器日志：
  - Docker 全局 `daemon.json` 已设置：
    - `log-driver: json-file`
    - `log-opts.max-size: 10m`
    - `log-opts.max-file: 5`
- Swap：
  - `2.0GiB`，挂载在 `/swap.img`
  - 已写入 `/etc/fstab`
- 网关反代：
  - 仅 `Nginx` HTTP 80
  - 未配置 HTTPS/TLS（按要求本阶段仅 IP 测试）

## 风险提醒（当前阶段接受）

- 未启用应用级鉴权（`/api/v1/*` 可直接访问）
- 未启用 TLS 证书
- 仅 Mock 逻辑，无真实收费 API 密钥

## 变更证据

- `sudo ufw status`
- `sudo fail2ban-client status`
- `cat /etc/docker/daemon.json`
- `swapon --show`
- `timedatectl status`

## 下一步建议（必须独立任务）

1. 增加 API 认证（设备级 token / mTLS）
2. HTTPS 与域名证书（Nginx 443）
3. 细化 fail2ban 规则（Nginx 403/419 限速）
4. 生产密钥与 provider 请求白名单
