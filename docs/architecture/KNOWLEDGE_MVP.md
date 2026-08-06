# Knowledge MVP

Updated: 2026-08-06

## Scope

Phase 1 uses only 10-30 human-confirmed FAQ entries. It does not scan all of `E:\work\积养家`, install Dify, build a vector database or ingest raw private documents.

## Data Source Rules

- FAQ entries must be manually reviewed.
- Each entry has explicit status: `approved`, `draft` or `mock`.
- Only `approved` entries can be used in store-facing answers.
- `draft` and `mock` entries are allowed only in tests or demos clearly labelled as such.
- No unverified price, medical, diagnostic, inventory or promotion claims.

## Schema

```yaml
version: 1
items:
  - id: faq-001
    status: approved
    question: "营业时间是什么？"
    aliases:
      - "几点开门"
      - "几点下班"
    answer: "请以门店当天公告为准。"
    tags: ["store"]
    source:
      type: manual
      owner: "human-review"
      reviewed_at: "2026-08-06"
    safety:
      allow_llm_rewrite: true
      prohibited_claims: []
```

## Retrieval

- Normalize Chinese punctuation, whitespace and common synonyms.
- Use exact and keyword matching first.
- Rank by alias hit count, tag relevance and question similarity.
- Return top 1-3 entries with IDs and confidence.
- Below threshold: return `no_match` and use transfer/fallback wording.

## LLM Grounding

Gateway passes only matched approved FAQ context to the LLM. The prompt must require:

- concise store-friendly answer;
- no unsupported claims;
- say "我暂时不能确认" when context is insufficient;
- suggest staff assistance for sensitive or unknown questions.

## Prohibited Topics

The knowledge layer must detect and avoid unsupported answers for:

- diagnosis, treatment guarantees or medical advice;
- exact pricing not in approved FAQ;
- stock/appointment availability not connected to live systems;
- internal finance, contracts, employee data or private customer data.

## Acceptance

- Schema validation passes.
- At least 10 approved entries before store pilot.
- Test set includes approved match, alias match, unknown, sensitive medical, price and internal-data questions.
- Evaluation report records correct/incorrect/fallback examples.
