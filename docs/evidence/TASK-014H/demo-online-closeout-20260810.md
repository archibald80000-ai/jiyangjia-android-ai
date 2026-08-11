# TASK-014H production Demo close-out

Executed: 2026-08-10 America/Chicago / 2026-08-11 UTC

## Decision

`BLOCKED`.

The production Gateway, v2.1 knowledge, real Provider dialogue and debug Demo APK pass internally. Public HTTP now reaches Nginx and returns the required `308`, but public HTTPS still resets before Nginx. Certbot renewal and browser APK download therefore cannot pass yet. This is not Android physical-device acceptance.

## Domain and TLS

- DNS A: `ai-jiyangjia.cloud -> 120.53.86.89`.
- Nginx config test: success; service active; 80/443 public and Gateway only on `127.0.0.1:8080`.
- Public HTTP: `308` to `https://ai-jiyangjia.cloud/`.
- Public HTTPS: connection reset before Nginx; the request does not appear in the Nginx access log.
- Certificate: valid Let's Encrypt certificate through 2026-11-05; renewal timer enabled and active.
- Renewal dry-run: failed because one ACME path still resolved through the Tencent webblock during access propagation. No further blind retries were made.

## Secrets and Providers

- Production secrets: `/opt/jiyangjia-ai/secrets/.env.local`, mode `600`.
- Production Compose now references that fixed absolute path and the Gateway was force-recreated.
- Readiness: Doubao ASR ready, Doubao TTS ready, Ark-compatible Doubao LLM ready, Doubao Embedding ready.
- No credential value was printed or committed.

## Knowledge activation

- Previous v2.2 state and server config backup: `/opt/jiyangjia-ai/backups/task014h-demo-online-20260811T034331Z`.
- Candidate: `/opt/jiyangjia-ai/candidates/task014h-v21-20260811T034520Z`.
- Imported only `import_batch_01.json`, then `import_batch_02.json`, using real Doubao Embedding.
- Production: 41 approved, 24 draft, 0 rejected; 65 chunks/embeddings/FAISS vectors; 2048 dimensions.
- Production 80-case policy result: 80/80, sources complete 80/80, draft leaks 0, matched responses 43, average search latency 176.2 ms.
- The active v2.1 switch used temporary files and atomic `mv`; the v2.2 rollback remains intact.

## Dialogue

- Five production `dialogue/text` requests returned HTTP 200, Doubao LLM/TTS, request IDs, audio IDs and downloadable `audio/mpeg`.
- One 553,038-byte Android-format `audio/wav` upload returned HTTP 200 after 31,625 ms and completed ASR -> RAG -> LLM -> TTS.
- ASR raw `鸡养家` normalized to `积养家`; approved source `faq_brand_001`; returned MP3 was 73,005 bytes.
- The production release lacked the already-tested short-query expansion. Only `gateway/app/knowledge.py` was synchronized after backup; `有什么产品` then matched `faq_service_007`, and `怎么体验` matched `faq_scenario_001`; both returned Doubao TTS audio with HTTP 200.
- Audio evidence used Doubao-generated synthetic speech, not a human microphone or Android device.

## Android Demo APK

- Build command: `gradlew.bat --no-daemon testDebugUnitTest lintDebug assembleDebug` with project JDK 17 and Android SDK.
- Result: build successful; debug signature verified with v1/v2 schemes.
- Package: `ai.jiyangjia.kiosk.debug`; version `0.1.0-development-debug`; min SDK 23; target SDK 35.
- Embedded Gateway URL: `https://ai-jiyangjia.cloud`.
- APK: 6,451,723 bytes; SHA-256 `C18EE46E93153E925B807E48D72BB7A8D66865C1247794B19B4DAA098D7B396E`.
- Server path: `/var/www/jiyangjia/downloads/jiyangjia-ai-demo.apk`.
- Target URL: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-demo.apk`.
- Server-local download: HTTP 200, correct APK MIME, attachment header, and matching hash.
- Public Chrome test: failed with connection closed before a download event; therefore the URL is not yet accepted as publicly downloadable.

## Next gate

After Tencent HTTPS/SNI propagation completes, execute exactly one public HTTPS health check, one Certbot renewal dry-run and one browser APK download. If all pass, TASK-014H may become `READY_FOR_ANDROID_DEMO`; TASK-015 remains a separate physical-device task.
