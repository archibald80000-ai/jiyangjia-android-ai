# TTS adapters

TASK-009 implements a real Doubao/Volcengine TTS adapter behind the Gateway TTS Provider interface, plus deterministic Mock tests.

The preferred Phase 1 route is the official V3 unidirectional synthesis endpoint for low-latency/realtime-style audio generation:

- `https://openspeech.bytedance.com/api/v3/tts/unidirectional`

Configure either API-key auth:

- `DOUBAO_TTS_API_KEY`

Or app/access-key auth:

- `DOUBAO_TTS_APP_ID`
- `DOUBAO_TTS_ACCESS_TOKEN`

Required synthesis configuration:

- `DOUBAO_TTS_SPEAKER`
- `DOUBAO_TTS_RESOURCE_ID`

Optional configuration:

- `DOUBAO_TTS_ENDPOINT`
- `DOUBAO_TTS_CLUSTER`
- `DOUBAO_TTS_ENCODING`
- `DOUBAO_TTS_SAMPLE_RATE`
- `DOUBAO_TTS_SPEECH_RATE`
- `DOUBAO_TTS_UID`
- `DOUBAO_TTS_TIMEOUT_SECONDS`
- `DOUBAO_TTS_VOICE_TYPE` for legacy v1 compatibility only

Do not place these values in Android code, Git, task evidence, or logs.

`.env.example` contains only placeholders. Use `.env.local` or server environment variables for real values, and set `JIYANGJIA_TTS_PROVIDER=doubao` only when the required values above are configured.

## Local Test

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider mock --text "您好"
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --text "您好"
```

For real verification, write output to an ignored temp path:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3
```

To use an external private env file without copying it into this repository:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "您好，欢迎来到积养家。" --output tmp\doubao-tts-test.mp3
```
