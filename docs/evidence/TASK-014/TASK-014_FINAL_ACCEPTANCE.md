# TASK-014 Final Acceptance

Date: 2026-08-07

## Result

`DONE`

Tencent Cloud Gateway at `120.53.86.89` passed the final real-provider deployment acceptance after a Gateway-only image rebuild and forced recreate.

## Build and runtime

- Host resources before build: about 1.2 GiB available memory, 2 GiB swap available, 38 GiB disk free.
- The inherited no-cache build was stopped after Docker reported `context canceled` and apt showed no useful progress.
- Debian and PyPI downloads were switched to Tencent Cloud mirrors with finite retries/timeouts.
- Gateway image: `sha256:0dbffb5b4a2e548690776c46ee617dc1b55b40bb990ab2df1a4807b2c0b24b72`.
- Container state after recreate: `running/healthy`.
- Online FFmpeg: `7.1.5-0+deb13u1`.
- Build log: `task014-gateway-build-final-20260807.txt`.

Gateway-only recreate command:

```bash
cd /opt/jiyangjia-ai/docker
docker compose up -d --no-deps --force-recreate gateway
```

## Provider readiness

- Secret file: `/opt/jiyangjia-ai/secrets/.env.local`.
- File mode: `600`.
- Compose points to `../secrets/.env.local`.
- Doubao ASR: ready.
- Doubao TTS: ready.
- Doubao/Ark LLM: ready.
- Doubao/Ark Embedding: ready.
- Evidence: `task014-provider-env-final-20260807.json`.

No secret values are included in the evidence.

## Knowledge cleanup

Eight TASK-014 deployment test records with conflicting business facts were changed from `approved` to `draft`. They included conflicting opening hours and incompatible service descriptions.

Final document counts:

- approved: 10;
- draft: 9;
- rejected: 1.

All approved entries are the controlled `manual://task012/faq_mvp_*` set. Backup before mutation:

`/opt/jiyangjia-ai/backups/task014-knowledge-cleanup-20260807-125648`

Evidence: `task014-knowledge-cleanup-final-20260807.json`.

## Final API acceptance

The acceptance runner was executed once against `http://120.53.86.89`.

Android WAV input matched the client implementation:

- PCM signed 16-bit little-endian;
- 16000 Hz;
- mono;
- 3.624 seconds;
- 116046 bytes.

Results:

| Flow | HTTP | Latency | ASR | Sources | Audio fetch |
|---|---:|---:|---|---:|---|
| text | 200 | 4165.91 ms | text | 2 | 200, audio/mpeg, 59373 bytes |
| Android WAV | 200 | 5370.95 ms | doubao | 1 | 200, audio/mpeg, 57837 bytes |
| MP3 | 200 | 4793.95 ms | doubao | 1 | 200, audio/mpeg, 59757 bytes |

Both audio inputs were transcribed as `请问积养家今天几点到几点营业？`. Each successful flow returned a request ID, knowledge sources, Doubao LLM answer, Doubao TTS result, audio ID and downloadable audio.

Complete response evidence: `task014-final-acceptance-20260807.json`.

## Rollback

- Knowledge rollback uses the backup directory above.
- Gateway rollback uses the prior Docker image retained on the server, followed by health/readiness verification.
- No raw recording, APK, Provider secret, SQLite database or FAISS index is committed to Git.
