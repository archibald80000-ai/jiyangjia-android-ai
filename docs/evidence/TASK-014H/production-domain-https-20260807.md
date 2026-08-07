# TASK-014H Production Domain and HTTPS Evidence

Date: 2026-08-07

## Result

Status: `BLOCKED_BY_TENCENT_WEBBLOCK_ICP`.

## Passed

- Local, Cloudflare `1.1.1.1` and Google `8.8.8.8` DNS resolvers returned `120.53.86.89` for `ai-jiyangjia.cloud`.
- Nginx 1.24 configuration test passed and service is active.
- Gateway container is healthy and publishes `127.0.0.1:8080` only.
- UFW allows 22/80/443 and does not allow 8080.
- Server-local canonical-domain checks returned: `/` 200, `/health` 200, `/api/v1/health` 200, `/api/v1/readiness` 200, `/admin` 302.
- Server-local HTTP returned 308 to `https://ai-jiyangjia.cloud/`.
- Readiness reported real ASR, TTS, LLM and Embedding providers ready.
- `ADMIN_TOKEN=configured`; `APP_ENV=production`. Values were not printed.
- Let's Encrypt certificate for `ai-jiyangjia.cloud` is valid until 2026-11-05.
- `snap.certbot.renew.timer` is enabled and active.
- Android `testDebugUnitTest` passed with JDK 17/Android SDK; generated debug BuildConfig uses `https://ai-jiyangjia.cloud` and disallows cleartext.
- Full Python regression passed: 86 tests; repository verification passed.
- Temporary rendered Compose output and staged `/tmp/task014h-*` files were deleted; the server secret file remains mode `600`.

## Failed public gate

- External `curl -I http://ai-jiyangjia.cloud` returned HTTP 302 to `https://dnspod.qcloud.com/static/webblock.html?d=ai-jiyangjia.cloud`, not the Nginx 308 response.
- External HTTPS connections with SNI `ai-jiyangjia.cloud` were reset before reaching Nginx.
- Certbot renewal dry-run failed because the ACME challenge was redirected to the same DNSPod webblock page.

The server configuration is ready, but the production domain is not publicly usable and automatic renewal is not validated. Complete Tencent Cloud ICP/domain access onboarding, then run the public acceptance and dry-run commands in `docs/server/operations.md` once.

## Rollback

- Backup: `/opt/jiyangjia-ai/backups/task014h-domain-20260807T103746Z`.
- Active release: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z`.
