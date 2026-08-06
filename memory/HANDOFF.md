# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-012_MINI_FAQ.md`
- Current status: `DONE`
- Current branch: `task/TASK-012-mini-faq`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; do not scan or bulk import)

## TASK-012 implemented

- `gateway.app.knowledge.SQLiteKnowledgeStore` now stores documents, chunks, FTS5 rows, embeddings and ingestion runs in SQLite.
- FAISS `IndexFlatIP` is rebuilt from provider vectors and optionally persisted to `JIYANGJIA_KNOWLEDGE_FAISS_PATH`.
- Explicit JSON/YAML/Markdown/TXT/PDF/DOCX knowledge parsing is supported. There was no bulk scan or import from `E:\work\积养家`.
- Customer search defaults to approved content only. Draft content requires `include_draft=True`; rejected content is excluded.
- Prohibited medical/price/promotion/inventory/member-balance/internal questions return the safe transfer answer before LLM generation.
- Knowledge search and dialogue responses include `sources` and `request_id`.
- Demo test FAQ and evaluation cases live under `knowledge-test/`.
- `scripts/evaluate_lightweight_rag.py` can evaluate with Mock or real Embedding providers.
- `gateway.app.llm.OpenAICompatibleEmbeddingProvider` now splits multimodal embedding batches into one request per text because the current Doubao multimodal route returns one vector per request.

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge -q`: 6 passed.
- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q`: 34 passed.
- `.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test`: Mock evaluation passed 24/24 cases.
- `.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test --provider doubao --env-file E:\work\ai-kefu\.env.local`: real Doubao/Ark Embedding evaluation passed 24/24 cases with 2048-dimensional vectors; values were not printed.
- Gateway API smoke passed for real embedding-backed `/api/v1/knowledge/index`, `/api/v1/knowledge/search` and `/api/v1/knowledge/status`.

## Evidence

- `docs/evidence/TASK-012/lightweight-rag.md`
- `docs/evidence/TASK-012/task012-pytest-knowledge-20260806.txt`
- `docs/evidence/TASK-012/task012-pytest-full-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-mock-20260806.txt`
- `docs/evidence/TASK-012/task012-evaluate-doubao-embedding-20260806.txt`
- `docs/evidence/TASK-012/task012-gateway-real-embedding-api-smoke-20260806.txt`

## Not verified

- Android end-to-end voice loop.
- Tencent Cloud deployment.
- Android 12 real-device acceptance.
- Formal production knowledge base beyond the scoped demo FAQ set.

## Next action

Continue exactly one next task: `TASK-013_END_TO_END_DIALOGUE.md`.

TASK-013 should connect Android recording, Gateway audio dialogue, Doubao ASR,
lightweight RAG, LLM answer generation, Doubao TTS, Android audio playback and
subtitle display. Do not claim Android 12 real-device success until hardware is
connected and tested.
