# TASK-011 evidence: LLM and Embedding providers

Updated: 2026-08-06

## Scope

TASK-011 added real OpenAI-compatible LLM and Embedding adapters behind the
Gateway Provider interfaces. It did not implement RAG parsing/indexing, Android
integration or deployment.

## Official documentation checked

- DeepSeek official API docs: `https://api-docs.deepseek.com/`
- DeepSeek Chat Completions docs: `https://api-docs.deepseek.com/api/create-chat-completion/`
- Volcengine Ark OpenAI-compatible docs: `https://www.volcengine.com/docs/82379/1330626`
- Volcengine text embedding API docs: `https://www.volcengine.com/docs/82379/1302003/`

## Implemented

- `gateway.app.llm.OpenAICompatibleLLMProvider`
- `gateway.app.llm.OpenAICompatibleEmbeddingProvider`
- Provider config for `deepseek`, `doubao`/`ark` and generic
  `openai-compatible`
- Safe error mapping for missing credentials and provider rejection
- Short-answer policy, low default temperature, max token cap, request ID header
  and finite timeout
- CLI smoke scripts:
  - `scripts/test_llm_provider.py`
  - `scripts/test_embedding_provider.py`
- Tests under `tests/llm/`

## Verification summary

| Check | Result | Evidence |
|---|---|---|
| Backend regression tests | PASS, 25 tests | `task011-pytest-final-20260806.txt` |
| Mock LLM CLI | PASS | `task011-mock-llm-cli-20260806.txt` |
| Mock Embedding CLI | PASS | `task011-mock-embedding-cli-20260806.txt` |
| DeepSeek config preflight | PASS, configured/missing only | `task011-deepseek-config-preflight-20260806.txt` |
| Doubao/Ark LLM config preflight | PASS, configured/missing only | `task011-doubao-llm-config-preflight-20260806.txt` |
| DeepSeek real LLM smoke | PASS, real API response, usage present | `task011-deepseek-real-llm-20260806.txt` |
| Doubao/Ark real LLM smoke | PASS, real API response, usage present | `task011-doubao-real-llm-20260806.txt` |
| Doubao Embedding config preflight | PASS with default model | `task011-doubao-embedding-config-preflight-20260806.txt` |
| Doubao Embedding real smoke, initial text model route | FAIL, provider rejected | `task011-doubao-embedding-real-call-rejected-20260806.txt` |
| Doubao Embedding real smoke, authorized multimodal route | PASS, 2048 dimensions | `task011-doubao-embedding-real-call-authorized-20260806.txt` |
| Backend regression after multimodal Embedding support | PASS, 27 tests | `task011-pytest-after-embedding-authorized-20260806.txt` |

## Real API result

Real LLM calls succeeded through both configured providers in
`E:\work\ai-kefu\.env.local`. Secret values were not printed or copied.

Initial Real Doubao/Ark text Embedding did not pass. The sanitized provider
error was:

```text
EMBEDDING_PROVIDER_REJECTED; http_status=404; provider_code=InvalidEndpointOrModel.NotFound; provider_type=Not Found
```

After account authorization, the verified current path is
`doubao-embedding-vision-251215`, routed to `/embeddings/multimodal` with typed
text input. The real smoke call returned one vector with 2048 dimensions and
usage metadata present.

## Status

`DONE`

## Verified final command

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "积养家门店服务时间"
```

Result: `ok=true`, `vector_count=1`, `dimensions=2048`, `usage_present=true`.

## Next task

Proceed to TASK-012 lightweight RAG.
