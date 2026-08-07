# Production Server

Updated: 2026-08-07

## Canonical addresses

- Domain: `ai-jiyangjia.cloud`
- Server: `120.53.86.89`
- Origin: `https://ai-jiyangjia.cloud`
- API base: `https://ai-jiyangjia.cloud/api/v1`
- Admin target: `https://ai-jiyangjia.cloud/admin`
- Health: `https://ai-jiyangjia.cloud/health`
- Readiness: `https://ai-jiyangjia.cloud/api/v1/readiness`

## Runtime

- Ubuntu 24.04, Nginx 1.24, Docker Compose Gateway.
- Nginx listens publicly on 80/443.
- Gateway port 8080 is bound to `127.0.0.1` only.
- Provider secrets remain at `/opt/jiyangjia-ai/secrets/.env.local`, mode `600`, outside Git.
- `ADMIN_TOKEN` is configured; its value must never be printed or committed.

## TLS status

- Let's Encrypt ECDSA certificate exists for `ai-jiyangjia.cloud` and expires 2026-11-05.
- `snap.certbot.renew.timer` is enabled and active.
- Renewal dry-run currently fails because Tencent redirects the ACME HTTP challenge to its DNSPod webblock page.

## Public blocker

Public HTTP currently returns a Tencent DNSPod webblock redirect and public HTTPS SNI is reset before reaching Nginx. Server-local `--resolve ...:127.0.0.1` checks pass. The domain is therefore not production-usable until ICP/domain access onboarding is released.
