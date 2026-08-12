# TASK-021 response persona production evidence

Date: 2026-08-12

## Change

- Gateway version: `0.3.3`
- Persona: `jiyangjia-neighbor-guide-v1`
- Modes: `concise`, `story`, `choice`
- Knowledge unchanged: 227 approved, 39 draft, 402 chunks/vectors, 2048 dimensions
- Real Providers: ASR/TTS/LLM/Embedding all `doubao` and ready
- Doubao Chat uses `thinking.type=disabled` for real-time response latency.

The vector index was not rebuilt. Retrieval query understanding, approved-context hydration and answer composition were improved independently from the knowledge facts.

## Automated tests

```text
python -m pytest tests/llm tests/gateway tests/e2e tests/knowledge/test_lightweight_rag.py -q
58 passed, 1 warning
```

The warning is a third-party FAISS/NumPy deprecation warning.

## Real public dialogue acceptance

Endpoint: `https://ai-jiyangjia.cloud/api/v1/dialogue/text`

| Mode | Question | Result | Latency | Sources | Audio |
| --- | --- | --- | ---: | --- | --- |
| concise | 积养家是什么？ | 200 | 6531 ms | 3 approved | MP3, 228333 bytes |
| story | 详细讲讲大有谷的故事。 | 200 | 8514 ms | 3 approved | MP3, 307629 bytes |
| choice | 送老人怎么选积养家的产品？ | 200 | 8424 ms | 1 approved | MP3, 250029 bytes |
| inventory | 大有谷现在有现货吗？ | 200 | 4505 ms | 0 | MP3, 113901 bytes |

Story request ID: `task021-production-story`; audio ID: `aud_172d81c47aa74e559bc0597ddcebd0d6`.

Accepted story facts were checked against the public `大有谷合作产品手册.html`. The inventory answer explicitly said current stock could not be confirmed and returned no source as false proof of real-time stock.

## Deployment and rollback

- Active release: `/opt/jiyangjia-ai/releases/release-task021-persona-20260812T155015Z`
- Backup: `/opt/jiyangjia-ai/backups/task021-persona-20260812T155015Z`
- Previous release: `/opt/jiyangjia-ai/releases/release-task021-public-gate-20260812T152345Z`
- Shared Provider env remained outside Git with mode 600; only LLM temperature `0.45` and max tokens `300` were updated.
- Only Gateway was recreated. SQLite, FAISS, Nginx and Android artifacts were not changed.

The first release switch could not write readiness evidence into the root-owned backup directory and automatically restored the previous env/release. The corrected switch wrote through `/tmp`, copied evidence with sudo and passed.

## Remaining gates

- Human judgement should continue to review tone on real store questions.
- Android 12 USB microphone, speaker, managed kiosk, formal signing/update and long-run acceptance remain under TASK-015.
