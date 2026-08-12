# TASK-014H - Production Domain and HTTPS

- **Status:** DONE
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

## Result (final verification 2026-08-12)

- DNS A records from the local resolver, Cloudflare and Google resolve to `120.53.86.89`.
- Nginx, the existing Let's Encrypt certificate, internal HTTPS routes, Gateway readiness and loopback-only port 8080 all pass on the server.
- Android production configuration is fixed to `https://ai-jiyangjia.cloud`; debug remains explicitly overridable.
- Public HTTP returns the required Nginx `308` redirect.
- Public HTTPS/TLS SNI reaches Nginx; `/health`, `/api/v1/health` and `/api/v1/readiness` return 200.
- The public APK endpoint returns 200 with the Android package MIME, attachment header and expected size.
- TLS negotiates 1.3 and presents the `ai-jiyangjia.cloud` certificate.
- Certbot renewal dry-run succeeds for `/etc/letsencrypt/live/ai-jiyangjia.cloud/fullchain.pem`.
- Internal production acceptance now additionally passes fixed secrets, all-real Providers, v2.1 at 41 approved / 24 draft / 65 x 2048 vectors, 80/80 search, real text/WAV dialogue and server-local APK download.

Status is `DONE`. Next task is TASK-015 Android 12 physical-device acceptance; it is not started by this task.
