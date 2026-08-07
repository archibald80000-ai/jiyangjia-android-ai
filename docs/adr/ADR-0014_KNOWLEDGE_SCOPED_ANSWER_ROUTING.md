# ADR-0014: Knowledge-scoped answer routing

- Status: Accepted
- Date: 2026-08-07

## Context

The original Gateway policy rejected price, medical and internal-information keywords before retrieval. That prevented approved boundary documents from answering questions they were written to cover. Conversely, unrelated general questions could reach vector search and be grounded in an irrelevant business document.

The owner clarified the product rule: questions explicitly about 积养家 or its related products and services require approved knowledge; if no approved evidence exists, the terminal must say it cannot confirm. Other questions should receive a contextual general answer instead of a blanket refusal.

## Decision

Use two answer scopes:

1. `jiyangjia`: explicit brand, store, product, service or customer-account questions search the business corpus. Customer responses may use only `approved` documents. Drafts are searched as a shadow corpus: when the strongest relevant evidence is draft, customer search returns no evidence rather than substituting a tangential approved document. A true no-match is reported to the LLM as `in_domain_unverified`, which must refuse to invent the business fact and direct the customer to staff.
2. `general`: unrelated questions skip the business knowledge search and enter the LLM as `general_answer`. The LLM should answer briefly and contextually. It must not claim access to private records or real-time systems and must frame medical, legal and financial content as general information rather than diagnosis or professional advice.

Retrieval requires a minimum combined evidence score. Keyword and vector scores are fused consistently, and low-confidence vector-only results are rejected. Draft and rejected content never appears in a customer response.

## Consequences

- Approved price, medical-boundary and service-policy documents can be used instead of being blocked by a global keyword list.
- Unknown 积养家 facts fail closed.
- Weather, writing, general health and similar questions cannot be accidentally grounded in the 积养家 corpus.
- The old 80-case labels `safe_transfer` and `no_match` are not a valid end-to-end oracle for the new two-scope behavior. Their approved-document and draft-isolation subsets remain valid retrieval checks; dialogue behavior is verified separately.
- Production activation remains a separate authorization and deployment step.
