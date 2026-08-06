# Embedding adapters

TASK-011 implements EmbeddingProvider through an OpenAI-compatible
`embeddings` HTTP contract. TASK-012 will use this adapter for the lightweight
RAG index; TASK-011 only verifies the provider path.

Supported provider values:

- `mock`: deterministic one-dimensional local test vector.
- `doubao` / `ark`: uses `DOUBAO_EMBEDDING_API_KEY` or `EMBEDDING_API_KEY`
  or `DOUBAO_API_KEY` / `ARK_API_KEY`, plus an explicit
  `DOUBAO_EMBEDDING_MODEL` or `EMBEDDING_MODEL`.
- `openai-compatible`: uses `OPENAI_COMPATIBLE_EMBEDDING_API_KEY` or
  `EMBEDDING_API_KEY` and an explicit embedding model.

The adapter returns only vector count and dimensions in CLI evidence by
default; full vectors are not printed into logs.

Manual smoke checks:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "积养家门店服务时间"
```

Do not print, commit or copy `.env.local` values.
