# ASR adapters

TASK-010 implements Mock ASR plus a Doubao/Volcengine WebSocket ASR adapter behind the Gateway ASR Provider interface.

Official documentation checked on 2026-08-06:

- `https://docs.volcengine.com/docs/6561/1354869?lang=zh`
- `https://www.volcengine.com/docs/6561/1354869`

The Phase 1 path is not always-on Android streaming. Android uploads one bounded recording to the Gateway, and the Gateway sends the bytes to Doubao ASR over WebSocket chunks.

Default endpoint:

- `wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_nostream`

Required auth is either:

- `DOUBAO_ASR_API_KEY`

Or:

- `DOUBAO_ASR_APP_ID`
- `DOUBAO_ASR_ACCESS_TOKEN`

Compatibility aliases accepted for the current private environment:

- `DOUBAO_REALTIME_APP_ID`
- `DOUBAO_REALTIME_ACCESS_TOKEN`

Required/important configuration:

- `DOUBAO_ASR_RESOURCE_ID`, default `volc.bigasr.sauc.duration`
- `DOUBAO_ASR_ENDPOINT`
- `DOUBAO_ASR_AUDIO_FORMAT`
- `DOUBAO_ASR_CHUNK_BYTES`
- `DOUBAO_ASR_TIMEOUT_SECONDS`

Do not place these values in Android code, Git, task evidence, or logs.

## Local Test

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_asr_provider.py --provider mock --file tmp\doubao-tts-test.mp3
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --file tmp\doubao-tts-test.mp3 --content-type audio/mpeg
```

Use only rights-cleared, non-private audio. Generated TTS smoke-test audio under `tmp\` is ignored and must not be committed.
