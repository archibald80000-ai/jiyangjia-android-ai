# Production Security Baseline

Updated: 2026-08-07

- UFW is active; allowed inbound ports are 22, 80 and 443.
- Nginx terminates TLS and proxies to `127.0.0.1:8080`.
- Docker does not publish Gateway port 8080 on public interfaces.
- Production Gateway runs with `APP_ENV=production` and a configured `ADMIN_TOKEN`.
- Provider secrets remain in `/opt/jiyangjia-ai/secrets/.env.local`, mode `600`, outside Git.
- Docker JSON log rotation remains `10m` x 5 files.
- Host time synchronization, fail2ban SSH jail and 2 GiB swap were verified in TASK-014.

## Open gates

- Tencent DNSPod webblock/ICP access control prevents public domain TLS acceptance.
- Certbot timer is active, but renewal dry-run fails until the webblock is released.
- Device authentication, rate limiting, monitoring/alerting and Android signed-release acceptance remain open.
