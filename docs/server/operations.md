# Gateway Operations

Updated: 2026-08-07

## Daily checks

```bash
docker ps --filter name=jiyangjia-gateway
docker logs --tail 120 jiyangjia-gateway
sudo nginx -t
systemctl is-active nginx
sudo ss -lntp | grep -E ':(80|443|8080)[[:space:]]'
sudo ufw status
sudo certbot certificates
systemctl status snap.certbot.renew.timer --no-pager
```

Expected port ownership: Nginx on 80/443 and Docker only on `127.0.0.1:8080`.

## Internal origin checks

These prove server configuration, not public reachability:

```bash
curl --resolve ai-jiyangjia.cloud:443:127.0.0.1 https://ai-jiyangjia.cloud/health
curl --resolve ai-jiyangjia.cloud:443:127.0.0.1 https://ai-jiyangjia.cloud/api/v1/health
curl --resolve ai-jiyangjia.cloud:443:127.0.0.1 https://ai-jiyangjia.cloud/api/v1/readiness
curl -I --resolve ai-jiyangjia.cloud:80:127.0.0.1 http://ai-jiyangjia.cloud/
```

## Public acceptance

Run from a network outside the server after ICP/access release:

```bash
curl -I http://ai-jiyangjia.cloud
curl https://ai-jiyangjia.cloud/health
curl https://ai-jiyangjia.cloud/api/v1/health
curl https://ai-jiyangjia.cloud/api/v1/readiness
curl -I https://ai-jiyangjia.cloud/admin
```

Expected: HTTP `308` to the canonical HTTPS host; health/readiness `200`; admin `302` to `/admin/system`. A redirect to `dnspod.qcloud.com/static/webblock.html` is a failed public gate.

## Certificate renewal

```bash
sudo certbot renew --cert-name ai-jiyangjia.cloud --dry-run \
  --non-interactive --no-random-sleep-on-renew
```

The timer being active is insufficient if dry-run fails.

## Demo APK download

```bash
curl --noproxy '*' -I --resolve ai-jiyangjia.cloud:443:127.0.0.1 \
  https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-demo.apk
sha256sum /var/www/jiyangjia/downloads/jiyangjia-ai-demo.apk
```

Expected headers include `application/vnd.android.package-archive` and `Content-Disposition: attachment`. The internal check does not replace a public browser download.

## Current rollback

Backup: `/opt/jiyangjia-ai/backups/task014h-domain-20260807T103746Z`.

```bash
BACKUP=/opt/jiyangjia-ai/backups/task014h-domain-20260807T103746Z
RELEASE=/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z

sudo cp -a "$BACKUP/nginx-conf.d.conf" /etc/nginx/conf.d/jiyangjia-ai.conf
sudo cp -a "$BACKUP/nginx-locations.conf" /etc/nginx/snippets/jiyangjia-gateway-locations.conf
sudo cp -a "$BACKUP/docker-compose.yml" "$RELEASE/deploy/docker-compose.yml"
sudo ln -sfn /etc/nginx/sites-available/jiyangjia-gateway /etc/nginx/sites-enabled/jiyangjia-gateway
sudo nginx -t && sudo systemctl reload nginx
cd "$RELEASE/deploy" && sudo docker compose up -d --no-deps --force-recreate gateway
```
