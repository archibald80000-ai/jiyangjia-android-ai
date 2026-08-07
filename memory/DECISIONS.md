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

New architectural decisions require a new ADR and an update to this table.
