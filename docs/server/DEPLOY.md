# Production Domain Deployment

## Files

- Nginx virtual hosts: `deploy/nginx-jiyangjia.conf`
- Shared proxy locations: `deploy/nginx-jiyangjia-locations.conf`
- Gateway Compose: `deploy/docker-compose.yml`
- Secrets: `/opt/jiyangjia-ai/secrets/.env.local` (server only)

## Installation

```bash
sudo install -m 0644 deploy/nginx-jiyangjia.conf /etc/nginx/conf.d/jiyangjia-ai.conf
sudo install -m 0644 deploy/nginx-jiyangjia-locations.conf /etc/nginx/snippets/jiyangjia-gateway-locations.conf
sudo nginx -t
sudo systemctl reload nginx

cd /opt/jiyangjia-ai/releases/<release>/deploy
sudo docker compose config >/tmp/jiyangjia-compose-rendered.yml
sudo docker compose up -d --no-deps --force-recreate gateway
```

The Compose publication must render as `127.0.0.1:8080`; never publish Gateway port 8080 on `0.0.0.0`.

## TLS

The current certificate uses Certbot webroot `/var/www/letsencrypt`. After ICP/access release, run:

```bash
sudo certbot renew --cert-name ai-jiyangjia.cloud --dry-run \
  --non-interactive --no-random-sleep-on-renew
```

Do not claim completion until this command and external HTTPS checks pass.
