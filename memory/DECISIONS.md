# Decision memory

| ID | Decision | Status | ADR |
|---|---|---|---|
| D-001 | Android client + remote services, not Windows EXE | Accepted | ADR-0001 |
| D-002 | Maintain `idle_video` and `livetalking_webrtc` modes | Accepted | ADR-0002 |
| D-003 | Start with 10–30 reviewed FAQ items; no vector DB | Accepted | ADR-0003 |
| D-004 | Keep LiveTalking as pinned upstream checkout with adapters/patches | Accepted | ADR-0004 |
| D-005 | Android V1 uses native kiosk shell plus WebView/WebRTC page | Accepted | ADR-0005 |
| D-006 | Wav2Lip is the first real-time model to reproduce when LiveTalking resumes; MuseTalk later | Superseded for Phase 1 | ADR-0006 / ADR-0008 |
| D-007 | Tencent CPU-only server runs gateway only, not GPU inference | Accepted | ADR-0007 |
| D-008 | Phase 1 ships idle-video voice FAQ MVP; LiveTalking/WebRTC/GPU inference deferred | Accepted | ADR-0008 |
| D-009 | Phase 1 knowledge layer is lightweight RAG with SQLite, FAISS, document parsers and embedding provider; Android hardware acceptance is deferred to TASK-015 | Accepted | ADR-0009 |
| D-010 | Phase 1 management uses the existing FastAPI/SQLite stack, explicit knowledge/media publish states and public asset/display contracts | Accepted | ADR-0010 |
| D-011 | Phase 1 display defaults to 1080x1920 portrait (9:16), while alternate Display Profiles remain selectable | Accepted | ADR-0011 |
| D-012 | Complete secure Android content sync, deterministic rendering, Gateway-proxied streaming ASR, managed kiosk and signed updates before physical acceptance | Accepted | ADR-0012 |
| D-013 | Provision the target as fully managed Device Owner and require automatic acoustic barge-in; click interrupt is fallback only | Accepted | ADR-0013 |
| D-014 | Use `https://ai-jiyangjia.cloud` as the canonical production Gateway origin; keep IP TLS only as a temporary rollback diagnostic | Accepted, operational | ADR-0014 |
| D-015 | Generate product knowledge from versioned public data and route unknown business terms through strong approved-corpus lexical evidence before hybrid retrieval | Accepted | ADR-0015 |
| D-016 | Separate the public phone demo APK from the managed store-kiosk APK; only the store variant may declare Home, boot, Device Admin and Lock Task behavior | Accepted | ADR-0016 |
| D-017 | Keep approved retrieval/facts separate from a versioned response-persona layer; disable Doubao deep thinking for real-time dialogue | Accepted | ADR-0017 |
| D-018 | Protect only the public navigation entries with a server-side PBKDF2/HMAC session gate and fixed redirect allowlist; keep the original external resources public | Accepted, operational | ADR-0018 |

New architectural decisions require a new ADR and an update to this table.
