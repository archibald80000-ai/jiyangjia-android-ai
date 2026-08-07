# Knowledge v2.1 scoped routing verification — 2026-08-07

## Outcome

`PARTIAL / ISOLATED UPLOAD VERIFIED / NOT PRODUCTION-ACTIVATED`.

The 65-document v2.1 candidate remains isolated from the existing local active database and production Gateway. It is served only on localhost port 8090 for acceptance. The owner-approved answer-routing change is implemented and verified with real Doubao Embedding and real Doubao LLM calls; TTS remained mock for this text-routing check.

## Accepted rule

- Questions explicitly about 积养家, its stores, products, services or customer-account facts may answer only from `approved` documents.
- If the strongest relevant material is draft or no approved evidence exists, no business fact is supplied and the answer advises asking staff.
- Other/general questions bypass the business knowledge corpus and receive a contextual LLM answer.
- General medical information is allowed with a professional-care boundary; diagnosis, private-record claims and fabricated real-time data remain prohibited.

Architecture record: `docs/adr/ADR-0014_KNOWLEDGE_SCOPED_ANSWER_ROUTING.md`.

## Candidate status

- Gateway: `127.0.0.1:8090` only; port 8080 and the existing 18081 demo were not changed.
- Documents: 65 total; 41 approved, 24 draft, 0 rejected.
- Chunks/embeddings/vectors: 65/65/65.
- Embedding: real Doubao, 2048 dimensions.
- Candidate SQLite SHA-256: `E8C744E4D2887A74D37CB23768390D449BE582B51D131ECA03D09D11EA834BCE`.
- Candidate FAISS SHA-256: `BE2E0969248B1020C04B6C6862C6A3CE0C5C50FAED1115657489516A70995B6C`.
- Pre-import rollback backup remains at ignored runtime path `var/knowledge-backups/pre-v2.1-20260807-034811/`.

## Real retrieval results

The source 80 cases were reused, but evaluated according to the accepted two-scope rule instead of the superseded global `safe_transfer` labels.

| Gate | Result |
|---|---:|
| Approved expected documents ranked first | 36/36 |
| Draft expected IDs excluded from customer results | 14/14 |
| Draft content returned to customer | 0 |
| General cases bypassed business search | 6/6 |
| Unknown explicit product `积养家有榴莲吗` | no match |
| Public request with `include_draft=true` | HTTP 422 rejected |

Thirteen of the fourteen draft-target cases returned no match. `你们有什么汤？` was answered from the separately approved `faq_soup_005` document, so it correctly used available approved evidence without exposing the draft `faq_soup_001` document.

## Real LLM dialogue checks

All calls returned HTTP 200:

| Case | Knowledge | Answer source | Result |
|---|---|---|---|
| `积养家是做什么的？` | matched approved | `knowledge_grounded` | grounded brand answer |
| `积养家有榴莲吗？` | no match | `in_domain_unverified` | explicitly unable to confirm; referred to staff |
| `帮我写个简短的请假条。` | no match | `general_answer` | produced a usable short template |
| `高血压平时应该注意什么？` | no match | `general_answer` | gave general precautions and a doctor boundary |

No credential value, recording or private customer data was written to evidence.

## Automated verification

```text
.venv/gateway-task008-py310/Scripts/python.exe -m pytest tests/knowledge tests/llm tests/gateway -q -k "not test_local_kiosk_demo_loads_real_presentation_and_dialogue_contracts"
47 passed, 1 deselected, 1 warning

.venv/gateway-task008-py310/Scripts/python.exe -m pytest -q
83 passed, 1 failed, 1 warning

.venv/gateway-task008-py310/Scripts/python.exe -m pytest -q -k "not test_local_kiosk_demo_loads_real_presentation_and_dialogue_contracts"
84 passed, 1 deselected, 1 warning
```

The one full-suite failure is outside TASK-017: the uncommitted TASK-015A kiosk page no longer contains the exact string asserted by `tests/gateway/test_gateway_api.py::test_local_kiosk_demo_loads_real_presentation_and_dialogue_contracts`. TASK-017 files and routing behavior are not involved. Those user changes were not overwritten or staged.

## Activation boundary

- The isolated import and routing implementation are ready for review.
- No production server was changed, no 8080 service was replaced, and the existing 18081 database remained unchanged.
- Production activation still requires an explicit deployment instruction and should preserve the recorded rollback backup.
