# MVP Deployment

Updated: 2026-08-06

## Deployment Target

Phase 1 deploys only the lightweight Gateway to the existing Tencent Cloud CPU server. No GPU inference, LiveTalking runtime, Wav2Lip or MuseTalk runs on this server.

## Server Components

- Gateway process.
- Reverse proxy with TLS.
- SQLite or simple file-backed config/data for Phase 1.
- Log rotation.
- Health check and process restart.
- Backup job for FAQ/config/log index, not raw recordings by default.

## Secrets

Secrets are stored only in server environment or an approved secret file outside Git:

- Doubao ASR credentials.
- Doubao TTS credentials.
- LLM provider API key/base URL/model.
- device token or mTLS material.

`.env.example` contains names only. `.env.local` values are never printed or committed.

## Logs

Gateway logs:

- timestamp;
- request_id;
- session_id;
- device_id hash or stable non-sensitive ID;
- provider names;
- latency;
- status/error code.

Logs must not contain provider tokens, cookies, raw audio, full private documents or unnecessary customer personal data.

## Backup

Backup these:

- approved FAQ file;
- server config template without secrets;
- deployment compose/service files;
- sanitized log index;
- release APK checksum and version metadata.

Do not backup raw recordings unless explicitly approved for a test.

## Rollback

- Keep previous Gateway artifact/config.
- Keep previous APK file and checksum.
- Rollback is: stop new Gateway, restore previous service config/artifact, health check, then reinstall previous APK if client regression exists.
- Android must keep local idle video usable during rollback.

## Monitoring

Minimum checks:

- `/api/v1/health`;
- process up/restart count;
- disk usage;
- memory usage on 4 GB server;
- provider failure rate;
- dialogue latency p50/p95;
- audio upload rejection count.

## Production Gate

Do not expose public deployment until:

- TLS configured;
- firewall/security group reviewed;
- device auth enabled;
- logs redacted;
- backup/rollback rehearsed;
- cost guard configured.
