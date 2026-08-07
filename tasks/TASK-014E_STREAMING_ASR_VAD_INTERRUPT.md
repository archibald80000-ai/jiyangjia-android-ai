# TASK-014E - Streaming ASR, VAD and Playback Interrupt

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-010 DONE, TASK-013 DONE, TASK-014C DONE
- **Allowed scope:** Gateway streaming ASR adapter/route, Android streaming audio client/state machine, tests and evidence

## Goal

Provide real-time partial transcription, automatic end-of-utterance and reliable interruption while keeping the existing WAV dialogue endpoint as fallback.

## Deliverables

- `StreamingASRProvider` interface and real Doubao bidirectional WebSocket implementation.
- Gateway `/api/v1/dialogue/stream` WebSocket contract.
- Android PCM frame sender and partial subtitle renderer.
- Proven WebRTC VAD on Gateway for speech start/end and bounded silence timeout.
- Final transcript normalization followed by existing RAG/LLM/TTS stages.
- Tap-to-interrupt: stop current TTS, cancel stale response and start a new stream.
- Automatic acoustic barge-in remains gated by real-device AEC/USB audio results.

## Acceptance

- Real Provider test returns partial and final text with request IDs.
- “积养家” final normalization remains accurate and retains `raw_text`.
- Normal speech auto-stops after configured silence and produces one answer.
- Stream failure falls back to buffered WAV when possible.
- Interrupted requests never resume stale audio.
- Latency, bytes, Provider stage and error evidence are saved without recording or secret leakage.
