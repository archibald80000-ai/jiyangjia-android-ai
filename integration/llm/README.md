# LLM adapters

TASK-011 implements real chat adapters through one OpenAI-compatible HTTP
contract. The Gateway selects the adapter with `JIYANGJIA_LLM_PROVIDER`.

Supported provider values:

- `mock`: deterministic local fallback for tests only.
- `deepseek`: uses `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL` and `DEEPSEEK_MODEL`.
- `doubao` / `ark`: uses `DOUBAO_API_KEY` or `ARK_API_KEY`, plus
  `DOUBAO_BASE_URL` / `ARK_BASE_URL` and `DOUBAO_MODEL` / `ARK_MODEL`.
- `openai-compatible`: uses `OPENAI_COMPATIBLE_API_KEY`,
  `OPENAI_COMPATIBLE_BASE_URL` and `OPENAI_COMPATIBLE_MODEL`.

The adapter sends non-streaming `chat/completions` requests with low
temperature, bounded `max_tokens`, request IDs and finite timeouts. Business
logic must not import vendor SDKs directly; add new vendors by mapping config
into this adapter or a small provider-specific wrapper.

Manual smoke checks:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_llm_provider.py --provider deepseek --env-file E:\work\ai-kefu\.env.local --check-config
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\test_llm_provider.py --provider deepseek --env-file E:\work\ai-kefu\.env.local --prompt "请用一句话说明你是谁。"
```

Do not print, commit or copy `.env.local` values.
