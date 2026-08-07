# Gateway Deployment Report

Updated: 2026-08-07

## Current deployment

- Server: `120.53.86.89`, Ubuntu 24.04, CPU-only.
- Canonical target: `https://ai-jiyangjia.cloud`.
- Gateway container: healthy; real ASR/TTS/LLM/Embedding readiness passes.
- Gateway bind: `127.0.0.1:8080` only.
- Public services: Nginx on 80/443; UFW allows 22/80/443.
- Secrets: `/opt/jiyangjia-ai/secrets/.env.local`, mode `600`, outside Git.
- `ADMIN_TOKEN` is configured and `APP_ENV=production`; values are not recorded.

## TLS and domain

- DNS A record resolves to `120.53.86.89` through multiple resolvers.
- Let's Encrypt certificate for `ai-jiyangjia.cloud` is valid until 2026-11-05.
- Server-local HTTPS checks pass for root, health, readiness and admin redirect.
- Public domain traffic is currently intercepted by Tencent DNSPod webblock; HTTPS SNI is reset and Certbot dry-run fails at the same interception.

## Status

TASK-014 Gateway deployment is DONE. TASK-014H canonical-domain rollout is `BLOCKED_BY_TENCENT_WEBBLOCK_ICP` and must not be treated as public HTTPS completion.

Evidence: `docs/evidence/TASK-014H/production-domain-https-20260807.md`.
