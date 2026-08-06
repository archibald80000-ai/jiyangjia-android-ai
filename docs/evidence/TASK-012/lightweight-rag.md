# TASK-012 Lightweight RAG Evidence

Updated: 2026-08-06

## Result

TASK-012 is DONE for local/backend acceptance.

Implemented:

- SQLite document/chunk metadata.
- SQLite FTS5 keyword index.
- FAISS Top-K vector retrieval.
- EmbeddingProvider-backed vector ingestion.
- Explicitly selected JSON/YAML/Markdown/TXT/PDF/DOCX knowledge parsing.
- Approved/draft/rejected status handling.
- Customer-facing approved-only search by default.
- Source citations in search and dialogue responses.
- Prohibited-topic policy for medical claims, prices/promotions/inventory, member balance and internal/private information.
- Safe transfer text for prohibited and uncertain questions.

Not claimed:

- Formal production knowledge base.
- Bulk import from `E:\work\积养家`.
- Android end-to-end integration.
- Tencent Cloud deployment.
- Android 12 real-device validation.

## Data

- Example FAQ file: `knowledge-test/faq_mvp_approved.example.json`
- Test cases: `knowledge-test/test_questions.example.json`
- Approved demo FAQ count: 10
- Extra non-customer examples: 1 draft, 1 rejected
- Evaluation cases: 24

All demo content is manually scoped test material. It does not claim real-time prices, inventory, promotions or medical treatment effects.

## Commands And Results

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge -q
```

Result: `6 passed, 1 warning`.

Log: `docs/evidence/TASK-012/task012-pytest-knowledge-20260806.txt`

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q
```

Result: `34 passed, 1 warning`.

Log: `docs/evidence/TASK-012/task012-pytest-full-20260806.txt`

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test
```

Result: `ok=true`, provider `mock`, `documents=12`, `chunks=11`, `cases=24`, `passed=24`, `failed=0`.

Log: `docs/evidence/TASK-012/task012-evaluate-mock-20260806.txt`

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\evaluate_lightweight_rag.py --data knowledge-test --provider doubao --env-file E:\work\ai-kefu\.env.local
```

Result: `ok=true`, provider `doubao`, `documents=12`, `chunks=11`, `cases=24`, `passed=24`, `failed=0`, vector dimensions `2048`.

Log: `docs/evidence/TASK-012/task012-evaluate-doubao-embedding-20260806.txt`

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe <gateway real embedding API smoke>
```

Result: `/api/v1/knowledge/index`, `/api/v1/knowledge/search` and `/api/v1/knowledge/status` succeeded with real Doubao/Ark embedding through Gateway. Reported vector index: ready, 1 vector, 2048 dimensions.

Log: `docs/evidence/TASK-012/task012-gateway-real-embedding-api-smoke-20260806.txt`

## Security

- `.env.local` remained outside the repository.
- Secret values were not printed in evidence.
- Generated runtime FAISS index under `var/` is ignored and can be rebuilt.
- No raw business-material directory was scanned or imported.

## Next

Proceed to `TASK-013_END_TO_END_DIALOGUE.md`: Android to Gateway end-to-end voice question-answer loop.
