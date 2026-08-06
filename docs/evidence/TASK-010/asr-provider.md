# TASK-010 ASR Provider Evidence

Date: 2026-08-06

## Official Documentation Checked

Official Volcengine/Doubao documentation entry points checked on 2026-08-06:

- `https://docs.volcengine.com/docs/6561/1354869?lang=zh` - ASR big-model WebSocket documentation provided by the user.
- `https://www.volcengine.com/docs/6561/1354869` - same official documentation entry without language query.

Implementation uses a Phase 1 file/bytes-to-WebSocket path:

- default endpoint: `wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_nostream`
- auth headers: either `X-Api-Key`, or `X-Api-App-Key` + `X-Api-Access-Key`
- required model/billing selector: `X-Api-Resource-Id`
- connection correlation: `X-Api-Connect-Id`
- binary frames: gzip-compressed JSON full-client request, then gzip-compressed audio-only packets with sequence flags
- default resource ID: `volc.bigasr.sauc.duration`

This is not Android always-on streaming. Android still uploads one bounded recording to the Gateway; the Gateway chunks and sends it to Doubao ASR.

## Implemented

- Added `DoubaoASRConfig` and `DoubaoASRProvider`.
- Added binary packet builder/parser for the Volcengine ASR WebSocket protocol.
- Added safe ASR missing-credential handling through `BLOCKED_PROVIDER_CREDENTIALS`.
- Added provider call error mapping for empty audio, provider errors, bad response and audio conversion failure.
- Added ffmpeg normalization for non-WAV/PCM input to 16 kHz mono PCM WAV before ASR.
- Added CLI test helper: `scripts/test_asr_provider.py`.
- Added CLI config preflight: `scripts/test_asr_provider.py --provider doubao --check-config`.
- Added `.env.example` ASR placeholders and integration notes.
- Gateway initializes Doubao ASR only when `JIYANGJIA_ASR_PROVIDER=doubao`.
- Gateway no longer silently downgrades configured Doubao ASR to Mock when credentials are missing.

## Verification

- `docs/evidence/TASK-010/task010-doubao-asr-config-preflight-20260806.txt`: external private env preflight returned configured app/access auth; values were not printed.
- `docs/evidence/TASK-010/task010-doubao-asr-real-call-wav-20260806.txt`: real Doubao ASR on normalized WAV returned text `您好，欢迎来到机养家。`.
- `docs/evidence/TASK-010/task010-doubao-asr-real-call-mp3-normalized-20260806.txt`: real Doubao ASR on MP3 input with Gateway normalization returned text `您好，欢迎来到机养家。`.
- `docs/evidence/TASK-010/task010-doubao-asr-debug-response-shape-20260806.txt`: sanitized response-shape probe confirmed `result.text` frame structure without printing secrets.
- `docs/evidence/TASK-010/task010-asr-wav-fixture-ffprobe-20260806.txt`: ffprobe verified WAV normalization output: 16000 Hz, mono, PCM s16le, 2.568 seconds, 82254 bytes.
- `docs/evidence/TASK-010/task010-mock-asr-cli-20260806.txt`: Mock ASR CLI returned deterministic mock text.
- `docs/evidence/TASK-010/task010-pytest-final-20260806.txt`: 16 tests passed.
- `docs/evidence/TASK-010/task010-final-pytest-20260806.txt`: 17 tests passed after timeout mapping coverage.
- `docs/evidence/TASK-010/task010-final-diff-check-20260806.txt`: `git diff --check` exit 0 with CRLF warning for `PROJECT_STATE.md`.
- `docs/evidence/TASK-010/task010-final-repository-verify-20260806.txt`: repository verification PASS.
- `docs/evidence/TASK-010/task010-final-secret-shape-scan-20260806.txt`: no API key/private-key/Bearer-token shape matches in TASK-010 changed/evidence files.
- `docs/evidence/TASK-010/task010-final-conflict-scan-20260806.txt`: no Git conflict markers at line start.

## Real API Status

DONE for TASK-010 provider acceptance.

Real provider verification used the external private env file `E:\work\ai-kefu\.env.local` without printing values:

- `DOUBAO_ASR_APP_ID`: configured through the ASR or realtime alias path
- `DOUBAO_ASR_ACCESS_TOKEN`: configured through the ASR or realtime alias path
- `DOUBAO_ASR_API_KEY`: missing but not required because app/access auth is configured
- `DOUBAO_ASR_RESOURCE_ID`: default

Known transcript issue:

- Expected test phrase: `您好，欢迎来到积养家。`
- Observed transcript: `您好，欢迎来到机养家。`
- Difference: `积` recognized as `机`; this should be corrected later through domain vocabulary, FAQ/RAG grounding, or post-ASR normalization policy. The real ASR path itself is verified.

The generated test audio and normalized WAV are stored under ignored `tmp\` and must not be committed.

## Reproduction

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_asr_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --file tmp\doubao-tts-test.mp3 --content-type audio/mpeg
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\asr tests\gateway tests\tts -q
```
