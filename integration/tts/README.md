# TTS adapters

TASK-009 implements a real Doubao/Volcengine HTTP TTS adapter behind the Gateway TTS Provider interface, plus deterministic Mock tests.

Real provider verification is currently blocked by missing credentials:

- `DOUBAO_TTS_APP_ID`
- `DOUBAO_TTS_ACCESS_TOKEN`
- `DOUBAO_TTS_VOICE_TYPE`

Optional configuration:

- `DOUBAO_TTS_ENDPOINT`
- `DOUBAO_TTS_CLUSTER`
- `DOUBAO_TTS_ENCODING`
- `DOUBAO_TTS_UID`
- `DOUBAO_TTS_TIMEOUT_SECONDS`

Do not place these values in Android code, Git, task evidence, or logs.

## Local Test

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider mock --text "您好"
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_tts_provider.py --provider doubao --text "您好"
```
