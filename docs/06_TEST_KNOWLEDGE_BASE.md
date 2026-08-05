# Mini knowledge test

The first knowledge layer is intentionally small.

## Content

- 10–30 reviewed customer-facing FAQs.
- Each item has ID, question variants, approved answer, status, source note and review date.
- Unknown prices, inventory, health claims and medical questions transfer to staff.

## Retrieval

Start with normalized exact/keyword matching. Do not install a vector database only to support a few entries. Add LLM fallback only after prompt and safety tests exist.

## Source policy

- Do not bulk-scan `E:\work\积养家`.
- A human selects and approves each source used in the test set.
- Files containing contracts, internal prices, personal information or credentials are excluded.
- Mock answers must be visibly marked in source data and never presented as confirmed production facts.

## Exit to formal knowledge base

Formal RAG work begins only after the end-to-end pilot is stable and the owner approves a source inventory, update workflow, factual boundaries and audit requirements.
