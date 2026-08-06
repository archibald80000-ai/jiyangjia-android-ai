# Gateway

Gateway is the Phase 1 FastAPI backend for the Android large-screen AI voice customer-service MVP.

## Current TASK-008 Status

Implemented and tested locally:

- `GET /health`
- `GET /api/v1/health`
- `GET /api/v1/client/config`
- `POST /api/v1/dialogue/text`
- `POST /api/v1/dialogue/audio`
- `POST /api/v1/knowledge/index`
- `POST /api/v1/knowledge/search`
- `GET /api/v1/knowledge/status`
- `GET /api/v1/audio/{audio_id}`

TASK-008 uses Mock ASR/TTS/LLM/Embedding providers. It does not call real Doubao, Volcengine Ark, OpenAI-compatible, or embedding APIs.

## Local Development

```powershell
py -3.10 -m venv .venv\gateway-task008-py310
.\.venv\gateway-task008-py310\Scripts\python.exe -m pip install -r gateway\requirements.txt
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway -q
.\.venv\gateway-task008-py310\Scripts\python.exe -m gateway --host 127.0.0.1 --port 18080
```

Port `8080` may be occupied locally; use another port for development when needed.

## Provider Route

- TASK-009: Doubao TTS.
- TASK-010: Doubao ASR.
- TASK-011: Doubao/Volcengine Ark LLM, OpenAI-compatible fallback LLM, Embedding API.
- TASK-012: SQLite + FAISS lightweight RAG with source citations.

Secrets must be loaded only from `.env.local` or server environment variables.
