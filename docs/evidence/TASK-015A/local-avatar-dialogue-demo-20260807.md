# TASK-015A Local Avatar Dialogue Evidence

Date: 2026-08-07

## Scope and safety

- User-authorized source: `E:\work\ai-kefu\资料库\人像背景.MOV`.
- The source file remained unchanged.
- Derived media, provider credentials, runtime databases, FAISS files and generated audio remain under ignored runtime paths and are not committed.
- This is an idle-video voice avatar. It is not lip sync, LiveTalking or real-time rendering.

## Prepared media

- Video: H.264, 1080x1920, 30 fps, yuv420p, silent, 21.300 seconds, 7,930,361 bytes.
- Video SHA-256: `7B19190A3A13A149780B3D9FC371D296EF356C92A8F8744119E573F673221AEB`.
- Background: JPG, 1080x1920, 239,140 bytes.
- Background SHA-256: `430DF518D6796F9AA5FAB2018A08D39F169D696227B6D43CB02D1CBE42EB073A`.
- Published asset IDs: `asset_63dd435b89694958` (video), `asset_d777ca4a174b4849` (background).
- Asset downloads from the local Gateway matched both source hashes.

## Display Profile

- ID: `display-1080x1920`.
- Orientation and size: portrait, 1080x1920.
- Scale mode: `fit`.
- Character anchor/scale: `(0.5, 0.5)`, `1.0`.
- Subtitle: 36 px, left/right 8%, bottom safe area 16%.
- Consult button: `(0.5, 0.9)`.

## Real local chain

- Isolated Gateway: `http://127.0.0.1:18084`.
- Provider readiness: Doubao ASR/TTS/LLM/Embedding all reported ready; no credential values were printed.
- Indexed one controlled approved brand FAQ with real 2048-dimensional embedding.
- Index request ID: `27aff980-9577-48da-94ba-ec85c6c23422`.
- Search request ID: `2d77c8bf-29d8-497c-92bf-7b9f16268bbc`; score `0.8056`; approved source returned.
- API dialogue request ID: `f1943930-f4c7-4bc7-bf4a-f86295b8b873`; RAG -> Doubao LLM -> Doubao TTS completed in 14,156 ms.
- Audio ID: `aud_44c6e026e9584789b1827dbb543d75e0`; `audio/mpeg`, 135,021 bytes; SHA-256 `6C92F8C00B9EF7ECA328D2C528D39D9656BCE3530ED6BBF8ADE44592356302DB`.

## Browser acceptance

- URL: `http://127.0.0.1:18084/demo/kiosk`.
- 9:16 test viewport: 540x960, representing the 1080x1920 Profile at 50% scale.
- Video state: 1080x1920, decoded (`readyState=4`), playing, no media error.
- Final UI dialogue request ID: `browser-999e98c6-10e5-4175-9967-c72b1f7a265d`.
- Visible source: `积养家品牌说明`.
- Subtitle/button overlap: false.
- Source/button overlap: false.
- Browser microphone capture has two completion paths: click `结束并发送`, or automatically stop/upload after confirmed speech followed by 3 seconds of continuous silence.
- Voice start requires two consecutive 100 ms samples above RMS `0.02`, reducing one-sample noise spikes. No detected speech means no 3-second empty upload; the existing 20-second maximum duration remains the fallback.
- The silence boundary was executed from the actual served JavaScript: no speech -> false, 2999 ms -> false, 3000 ms -> true.
- Microphone permission and a spoken recording still require manual user acceptance.

## Automated verification

```text
.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway\test_gateway_api.py -q
8 passed, 1 FAISS dependency deprecation warning
```

The served JavaScript passed `node --check`; its extracted silence policy passed the 0/2999/3000 ms boundary test. `git diff --check` passed for the implementation. Android 12 physical-device behavior was not tested and remains under TASK-015.
