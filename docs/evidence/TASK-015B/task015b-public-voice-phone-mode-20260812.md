# TASK-015B public voice and phone-safe APK evidence

- Date: 2026-08-12
- Branch: `codex/TASK-015B-public-voice-phone-mode`
- Production: `https://ai-jiyangjia.cloud`
- Rollback: `/opt/jiyangjia-ai/backups/task015b-20260812T090810Z`
- Image rollback tag: `jiyangjia-gateway:backup-task015b-20260812T090810Z`

## Gateway and browser

- Targeted Gateway/stream tests: `14 passed`.
- Public HTTP `/`: `308` to HTTPS.
- HTTPS `/` and `/demo/kiosk`: `200 text/html`.
- Root mode: `public`; kiosk mode: `kiosk`.
- Response header: `Permissions-Policy: microphone=(self)`.
- Production Chrome check: avatar video loaded, public navigation visible, kiosk navigation hidden, no console errors and no failed requests.
- Malformed WebSocket start with string generation returned `INVALID_START`.
- Real streaming request: `task015b-rag-1786526234903`.
- Flow: ready -> speech_started -> 2 partial transcripts -> Doubao final `积养家是什么？` -> answering heartbeat -> answer -> TTS ready.
- Sources: `faq_brand_002`, `faq_brand_001`, `faq_food_001`; all use `knowledge://` URIs.
- Audio: `aud_c5a43b49ab2f42f49233dcbfd33df948`, `audio/mpeg`, fetch `200`, `137325` bytes, SHA-256 `90B5B13F72AFE40F87B367A766DC123A5DC2DFFD53DE324873664D084D7BA74A`.
- Provider readiness remained true for Doubao ASR/TTS/LLM/Embedding. Knowledge remained 227 approved, 24 draft and 387 x 2048 FAISS vectors.

The streaming input was locally synthesized Chinese speech and contains no customer recording. Browser permission, human speech and acoustic echo remain manual checks.

## Android artifacts

Phone experience:

- Package: `ai.jiyangjia.kiosk.debug`.
- Version: `9` / `0.1.8`.
- Public URL: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-digital-human.apk`.
- Size: `6402961` bytes.
- SHA-256: `63E21EBC75030EA3AEEFD24C53D22349791E23707A150BDD4DA32C0BF3BAB31D`.
- Manifest has no Home category, custom BootReceiver, Device Admin receiver, `RECEIVE_BOOT_COMPLETED` or `REQUEST_INSTALL_PACKAGES`.

Store kiosk:

- Package: `ai.jiyangjia.kiosk.store`.
- Version: `9` / `0.1.8`.
- Public URL: `https://ai-jiyangjia.cloud/downloads/jiyangjia-ai-store-kiosk.apk`.
- Size: `6388417` bytes.
- SHA-256: `F2963F0411BD706996B9D6B95B74ACC17917F860578C9998C9BEFC7B59CE7BDC`.
- Manifest retains Home, boot, Device Admin, Lock Task support and controlled package installation.

Both APKs passed unit tests, Lint, assembly, AAPT package inspection and v1/v2 debug-signature verification. They use the existing Android debug certificate; formal production signing is still pending.

## Android 13 smoke and blocker

- Device: Xiaomi `M2102J2SC`, Android 13.
- The APK downloaded from the public URL installed successfully before instrumentation.
- Three cold launches succeeded in 432-448 ms with live processes and no `FATAL EXCEPTION`.
- Home focused `com.miui.home`; recents remained in the MIUI launcher task surface; notification shade focused `NotificationShade`.
- Package inspection reported Home, Device Admin and package-install capabilities absent.
- `connectedPhoneDemoDebugAndroidTest` built its test APK but MIUI rejected installation with `INSTALL_FAILED_USER_RESTRICTED: Install canceled by user`; zero instrumentation tests ran.
- The failed test installation removed the app package. A subsequent reinstall was also rejected by the same user restriction. The phone must be unlocked and the USB-install confirmation accepted before rerunning exactly once.

## Full-suite note

The backend suite produced `112 passed / 1 failed`. The only failure is a pre-existing v2.3 manifest byte/hash mismatch: the `58e270c` Git blob for `knowledge-public/v2.3/import_all.json` is `382478` bytes while its manifest records `384241`. TASK-015B did not modify knowledge files and did not rewrite the published package.

## Final verification commands

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest `
  tests\asr\test_streaming_asr.py tests\gateway\test_gateway_api.py -q

.\android-app\gradlew.bat -p android-app `
  testPhoneDemoDebugUnitTest testStoreKioskDebugUnitTest `
  lintPhoneDemoDebug lintStoreKioskDebug `
  assemblePhoneDemoDebug assembleStoreKioskDebug

.\scripts\verify_repository.ps1
git diff --check
```

Final result: Gateway `14 passed`; both Android variants completed unit test, Lint and assemble; repository verification passed; `git diff --check` passed. AAPT reported the expected package/version/label for both APKs and `apksigner` verified v1/v2 debug signatures. Public HTTPS root, kiosk, health and both APK endpoints returned `200`; response lengths matched the published APK files.
