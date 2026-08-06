# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-011_LLM_ROUTER.md`
- Current status: `DONE`
- Current branch: `task/TASK-011-llm-router`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## TASK-011 implemented

- `gateway.app.llm.OpenAICompatibleLLMProvider`
- `gateway.app.llm.OpenAICompatibleEmbeddingProvider`
- Provider config for:
  - `deepseek`
  - `doubao` / `ark` / `volcengine`
  - `openai-compatible`
- Gateway LLM provider selection and safe missing-credential/error mapping.
- Gateway knowledge status reports embedding readiness/missing config.
- Doubao/Ark Embedding route selection:
  - plain text model IDs use `/embeddings`;
  - `vision` or `multimodal` model IDs use `/embeddings/multimodal`;
  - multimodal text input is wrapped as typed text parts.
- CLI helpers:
  - `scripts/test_llm_provider.py`
  - `scripts/test_embedding_provider.py`
- Tests under `tests/llm`.

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\llm tests\gateway tests\asr tests\tts -q`: 27 passed.
- Mock LLM CLI succeeded.
- Mock Embedding CLI succeeded.
- DeepSeek config preflight succeeded with configured/missing status only.
- Doubao/Volcengine Ark LLM config preflight succeeded with configured/missing status only.
- Real DeepSeek LLM smoke call succeeded using private external env `E:\work\ai-kefu\.env.local`; values were not printed.
- Real Doubao/Volcengine Ark LLM smoke call succeeded using private external env `E:\work\ai-kefu\.env.local`; values were not printed.
- Real Doubao/Ark Embedding smoke call succeeded using private external env; values were not printed.
- Verified default Embedding model path: `doubao-embedding-vision-251215`.
- Verified Embedding result: 1 vector, 2048 dimensions, usage metadata present.

## Historical note

- Earlier plain text candidates such as `doubao-embedding-text-240515` returned
  `InvalidEndpointOrModel.NotFound` for this account/path.
- The accepted path for the current account is the multimodal embedding route.

## Evidence

- `docs/evidence/TASK-011/llm-provider.md`
- `docs/evidence/TASK-011/task011-pytest-final-20260806.txt`
- `docs/evidence/TASK-011/task011-deepseek-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-real-call-authorized-20260806.txt`
- `docs/evidence/TASK-011/task011-pytest-after-embedding-authorized-20260806.txt`

## Not verified

- FAISS index build/search with real embeddings.
- Approved FAQ/document ingestion.
- Android end-to-end voice loop.
- Tencent Cloud deployment.
- Android 12 real-device acceptance.

## Next action

Continue exactly one next task: `TASK-012_MINI_FAQ.md`.

TASK-012 should build lightweight RAG with SQLite/FTS/FAISS, approved
FAQ/document ingestion, real EmbeddingProvider vectors and source citations.
