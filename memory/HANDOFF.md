# Handoff

Updated: 2026-08-06

## Current task

- Current task: `TASK-011_LLM_ROUTER.md`
- Current status: `PARTIAL`
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
- Gateway knowledge status now reports embedding readiness/missing config.
- CLI helpers:
  - `scripts/test_llm_provider.py`
  - `scripts/test_embedding_provider.py`
- Tests under `tests/llm`.

## Verified

- `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\llm tests\gateway tests\asr tests\tts -q`: 25 passed.
- Mock LLM CLI succeeded.
- Mock Embedding CLI succeeded.
- DeepSeek config preflight succeeded with configured/missing status only.
- Doubao/Volcengine Ark LLM config preflight succeeded with configured/missing status only.
- Real DeepSeek LLM smoke call succeeded using private external env `E:\work\ai-kefu\.env.local`; values were not printed.
- Real Doubao/Volcengine Ark LLM smoke call succeeded using private external env `E:\work\ai-kefu\.env.local`; values were not printed.
- Doubao/Ark Embedding config preflight succeeded with the default `doubao-embedding-text-240515` model slot.

## Blocked

- Real Doubao/Ark Embedding smoke call failed:

```text
EMBEDDING_PROVIDER_REJECTED
http_status=404
provider_code=InvalidEndpointOrModel.NotFound
provider_type=Not Found
```

- Additional attempts using `doubao-embedding-text-240715`,
  `doubao-embedding-large-text-250515` and the private `ARK_API_KEY_RESOURCE_ID`
  value as an in-process model candidate were also rejected. Those values were
  not printed.

## Evidence

- `docs/evidence/TASK-011/llm-provider.md`
- `docs/evidence/TASK-011/task011-pytest-final-20260806.txt`
- `docs/evidence/TASK-011/task011-mock-llm-cli-20260806.txt`
- `docs/evidence/TASK-011/task011-mock-embedding-cli-20260806.txt`
- `docs/evidence/TASK-011/task011-deepseek-config-preflight-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-llm-config-preflight-20260806.txt`
- `docs/evidence/TASK-011/task011-deepseek-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-real-llm-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-config-preflight-20260806.txt`
- `docs/evidence/TASK-011/task011-doubao-embedding-real-call-rejected-20260806.txt`

## Not verified

- Real Embedding API success.
- FAISS index build/search with real embeddings.
- Android end-to-end voice loop.
- Tencent Cloud deployment.
- Android 12 real-device acceptance.

## Next action

Continue exactly one next action: configure a verified enabled Ark/Doubao
embedding model or endpoint in private env, then rerun:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "积养家门店服务时间"
```

Do not start TASK-012 until real Embedding is verified or explicitly waived.
