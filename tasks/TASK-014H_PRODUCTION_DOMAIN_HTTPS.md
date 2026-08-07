# TASK-014H - Production Domain and HTTPS

- **Status:** BLOCKED
- **Priority:** P0
- **Dependencies:** TASK-014 DONE, DNS control for `ai-jiyangjia.cloud`, Tencent Cloud host access

## Goal

Make `https://ai-jiyangjia.cloud` the canonical production Gateway address across DNS, Nginx, TLS, Android and operations documentation.

## Acceptance

- Public DNS A record resolves to `120.53.86.89` from multiple resolvers.
- Port 80 redirects to the canonical HTTPS host, except the ACME challenge path.
- A valid Let's Encrypt certificate for `ai-jiyangjia.cloud` is installed and renewal is enabled.
- Nginx proxies the domain to `127.0.0.1:8080`; Docker does not publish port 8080 on public interfaces.
- `/health`, `/api/v1/health`, `/api/v1/readiness` and `/admin` are reachable through the production domain.
- Production Android builds use `https://ai-jiyangjia.cloud`; debug builds retain an explicit local override.
- Secrets remain external to Git and no provider values appear in evidence.

## Rollback

- Back up active Nginx, location snippet and Compose files before replacement.
- If `nginx -t`, container recreation or health checks fail, restore the backup and reload Nginx/recreate Gateway.
- Keep the IP certificate virtual host temporarily for rollback diagnostics; it is not an Android production dependency.

## Stop condition

If public DNS, TLS handshake, Nginx or Gateway checks do not all pass, keep this task `PARTIAL` or `BLOCKED` and record the exact failed layer.

## Result (2026-08-07)

- DNS A records from the local resolver, Cloudflare and Google resolve to `120.53.86.89`.
- Nginx, the existing Let's Encrypt certificate, internal HTTPS routes, Gateway readiness and loopback-only port 8080 all pass on the server.
- Android production configuration is fixed to `https://ai-jiyangjia.cloud`; debug remains explicitly overridable.
- Public HTTP is intercepted with a redirect to `dnspod.qcloud.com/static/webblock.html`, and public HTTPS SNI is reset before Nginx.
- Certbot renewal dry-run fails because the ACME challenge is also redirected to the DNSPod webblock page.

Status is `BLOCKED_BY_TENCENT_WEBBLOCK_ICP`. Do not mark DONE until Tencent Cloud domain access/ICP onboarding is approved and all public checks plus Certbot dry-run pass.
