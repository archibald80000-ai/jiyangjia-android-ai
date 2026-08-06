# ADR-0009: Lightweight RAG and Real Provider Route

Date: 2026-08-06

## Status

Accepted

## Context

The project needs to reach an Android large-screen AI voice customer-service MVP quickly. LiveTalking, Wav2Lip, MuseTalk, realtime lip-sync and GPU inference are not required for the first releasable flow. Android hardware validation is important but should not block local Gateway/provider/RAG development.

## Decision

- Defer LiveTalking, Wav2Lip, MuseTalk, WebRTC digital human and GPU inference to a later enhancement phase.
- Do not use Dify, LangFlow, Flowise or other heavy orchestration platforms in Phase 1.
- Build the MVP backend as FastAPI Gateway plus Provider Adapters.
- Use SQLite for knowledge metadata and local FAISS for vector retrieval in the lightweight RAG stage.
- Use Markdown/TXT/PDF/DOCX as approved document inputs.
- Require real Doubao ASR, real Doubao TTS, real Doubao/Volcengine Ark LLM, OpenAI-compatible fallback LLM and Embedding API evidence before claiming real provider completion.
- Load provider secrets only from `.env.local` or server environment variables.
- Defer Android real-device acceptance to TASK-015; local code and automated tests continue first.

## Consequences

- TASK-008 provides the Gateway/API/Provider skeleton and Mock orchestration only.
- TASK-009 to TASK-012 replace Mock providers and retrieval with real adapters and lightweight RAG.
- TASK-013 connects Android to the completed local backend loop.
- TASK-014 deploys after local tests pass.
- TASK-015 validates the Android 12 large display, USB microphone and speakers.
