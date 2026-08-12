# TASK-020H knowledge v2.4 integrity and production sync

Date: 2026-08-12

## Result

`DONE / PRODUCTION_PUBLISHED`.

The authorized 135-file v2.3 site mirror matched its read-only source byte-for-byte. The v2.3 generator now emits deterministic UTF-8/LF JSON, repairing all manifest size/hash records without changing its 251 knowledge documents.

The user then authorized two additional HTML sources. v2.4 preserves v2.3 and adds two collection summaries plus thirteen detailed soup records. All 15 additions are `draft` because the source pages require final-menu review and contain special-population or health-adjacent wording. They are indexed for review but excluded from customer retrieval.

## Public packages

- v2.3 source mirror: 135/135 files, zero hash mismatches.
- v2.4 documents: 266 total; 227 approved, 39 draft, 0 rejected.
- v2.4 additions: 15 draft records; one incremental import batch.
- Source `积养家七膳煨汤｜七款汤膳故事.html`: 28,747 bytes, SHA-256 `FD1AC92993CC60358B062A4612BC7CA7F36CF6ED207818FFB4A46EED527F3C71`.
- Source `积养家瓦罐六膳｜六款瓦罐汤故事.html`: 26,663 bytes, SHA-256 `7C55036F23C215734178472DA5819CE56A96B9AE299710754D4EF14B568D2AD2`.
- v2.4 normalized document fingerprint: `6af1d79eb1f4c25f19f124a78900f280194aa64f905d6048381b8033ecfd912a`.

## Local tests

```text
pytest v2.4/v2.3/v2.2/lightweight-rag/answer-policy
46 passed, 1 third-party FAISS/NumPy deprecation warning
```

## Production backup and package

- Backup: `/opt/jiyangjia-ai/backups/task020h-20260812T150643Z`.
- Backup SQLite SHA-256: `820167dde9994a302b9adf2b48f25e53b1c2f2719e8c9f8097ca25d56e8d8ddd`.
- Backup FAISS SHA-256: `9b47c558cbad313b6e63e092d2f4b87cf39a8f6c72290ee756f1609be33b4284`.
- Server package: `/opt/jiyangjia-ai/knowledge-public/v2.4-6af1d79eb1f4-20260812T151153Z`.
- Candidate and production SQLite SHA-256: `c296dff420724dfb5f085245ca4e3bcea80a210505bf089377451fbbefd75b41`.
- Candidate and production FAISS SHA-256: `ef17bfb0d3f27221a93d21557a6c3c20936c2da45f25b86c58a99c53346849a9`.
- Provider readiness: real Doubao ASR, TTS, LLM and Embedding all ready; no secret values were printed.

## Real acceptance

- Delta import: 15 documents, 15 chunks, real Doubao Embedding.
- Final production: 227 approved, 39 draft, 402 chunks/embeddings/vectors, 2048 dimensions; SQLite integrity `ok`.
- Existing approved product Top-3: 141/141; sources 141/141; draft leaks 0.
- New draft isolation: 43/43 requests completed; draft leaks 0.
- Real dialogue question: `圣牧有机酸奶是什么？`.
- request_id: `task020h-production-dialogue`.
- Knowledge: matched approved source `site_product_shengmu-yogurt`.
- Providers: Doubao LLM and Doubao TTS.
- audio_id: `aud_8f8871149d31444585073316dbc9cb6c`.
- Audio fetch: HTTP 200, `audio/mpeg`, 180,909 bytes, SHA-256 `B024F2770751A8AC3D38EEE1562D71CEDF40502E96537505FEA846538B1F49F8`.

## Rollback

Stop the Gateway, restore both `jiyangjia.db` and `faiss.index` from the TASK-020H backup to same-filesystem temporary names, atomically replace both active files, then restart and verify readiness. Runtime databases, indexes, audio and secrets are not committed to Git.
