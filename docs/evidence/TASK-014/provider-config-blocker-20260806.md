# TASK-014 Provider Configuration Blocker

Date: 2026-08-06

## What This Is

The current Tencent Cloud blocker is the real Provider configuration chain, not the upload path.

The Gateway process reaches the application layer, but real dialogue calls are stopped before ASR/LLM/TTS/Embedding execution because required `DOUBAO_*`, `ARK_*` or OpenAI-compatible environment variables are missing or not loaded by the running container.

## Observed Shape

- Docker Compose starts and the container is healthy.
- `GET /health`, `GET /api/v1/health`, `GET /api/v1/client/config` and knowledge endpoints can return 200.
- `POST /api/v1/dialogue/text` returns 503 with `BLOCKED_PROVIDER_CREDENTIALS`.
- `POST /api/v1/dialogue/audio` also returns 503 after request parsing reaches Provider checks.
- No `audio_id` can be fetched while dialogue fails before TTS.

## Decision

Stop repeating dialogue/upload tests until readiness shows the real Providers are configured.

The next server step is:

1. Verify `/opt/jiyangjia-ai/secrets/.env.local` exists and has mode `600`, without printing values.
2. Verify Docker Compose `env_file` points to `../secrets/.env.local`.
3. Run `scripts/check_provider_env.py --require-real-mvp` and stop if it reports missing fields.
4. Rebuild/restart the container.
5. Call `GET /api/v1/readiness` and record configured/missing status.
6. Run exactly one full text dialogue and one full audio dialogue acceptance.

## Gateway Hardening

This task adds:

- `GET /api/v1/readiness`, returning Provider readiness and missing variable names without values.
- `scripts/check_provider_env.py`, checking the env file and Compose path without printing values.
- `failed_stage` in credential-blocked 503 responses:
  - `asr_provider_config`
  - `embedding_provider_config`
  - `llm_provider_config`
  - `tts_provider_config`

This prevents downstream Provider failures from being misreported as upload failures.
