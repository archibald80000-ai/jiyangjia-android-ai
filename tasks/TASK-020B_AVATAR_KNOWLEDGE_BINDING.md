# TASK-020B formal knowledge and avatar demo binding

Executed: 2026-08-07 America/Chicago (`20260808T025409Z` UTC runtime stamp)

## Goal

Bind the accepted TASK-020A SQLite/FAISS candidate to the isolated 9:16 avatar demo, preserve the previous demo state, and verify one real ASR -> RAG -> LLM -> TTS dialogue through both API and browser surfaces.

## Acceptance

- Previous avatar admin, knowledge and FAISS state has a timestamped rollback copy.
- Port `18084` uses real Doubao ASR, TTS, LLM and Embedding providers without exposing credentials.
- The bound knowledge status is 41 approved, 24 draft, 65 chunks and 65 vectors at 2048 dimensions.
- The published 1080x1920 video/background and default portrait Display Profile remain active.
- A real WAV request normalizes an observed brand homophone, returns approved sources and produces downloadable TTS audio.
- Public source metadata does not expose local source-file paths.
- The browser demo loads, plays the portrait video, answers a text question, displays sources and returns to idle.
- Databases, FAISS indexes, recordings, generated audio and source documents remain ignored and outside Git.

## Decision

`DONE` for local avatar/knowledge binding. This task does not claim Tencent production publication, public HTTPS recovery, browser microphone permission or Android 12 physical-device acceptance.

## Evidence

See `docs/evidence/TASK-020B/avatar-knowledge-binding-20260807.md`.
