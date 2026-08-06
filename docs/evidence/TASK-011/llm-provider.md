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
| Doubao Embedding real smoke | FAIL, provider rejected | `task011-doubao-embedding-real-call-rejected-20260806.txt` |

## Real API result

Real LLM calls succeeded through both configured providers in
`E:\work\ai-kefu\.env.local`. Secret values were not printed or copied.

Real Doubao/Ark Embedding did not pass. The sanitized provider error was:

```text
EMBEDDING_PROVIDER_REJECTED; http_status=404; provider_code=InvalidEndpointOrModel.NotFound; provider_type=Not Found
```

This means TASK-011 is useful but not fully accepted as a real Embedding stage
until an enabled embedding endpoint/model is configured, for example a verified
Ark text embedding model or endpoint ID with account access.

## Status

`PARTIAL`

## Next unblock action

Configure a real enabled Embedding model/endpoint in private env, preferably:

- `DOUBAO_EMBEDDING_MODEL` or `EMBEDDING_MODEL`
- and, if needed, `DOUBAO_EMBEDDING_BASE_URL` or `EMBEDDING_BASE_URL`

Then rerun:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_embedding_provider.py --provider doubao --env-file E:\work\ai-kefu\.env.local --text "积养家门店服务时间"
```
