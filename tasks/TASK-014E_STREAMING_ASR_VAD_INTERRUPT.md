# TASK-014E - Streaming ASR, VAD and Playback Interrupt

- **Status:** PARTIAL
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
- Automatic acoustic barge-in is implemented as the required primary behavior; AEC/USB audio acceptance remains a release gate and click interrupt remains the fallback control.

## Acceptance

- Real Provider test returns partial and final text with request IDs.
- “积养家” final normalization remains accurate and retains `raw_text`.
- Normal speech auto-stops after configured silence and produces one answer.
- Stream failure falls back to buffered WAV when possible.
- Interrupted requests never resume stale audio.
- Latency, bytes, Provider stage and error evidence are saved without recording or secret leakage.

## Implementation result (2026-08-07)

- Gateway exposes `/api/v1/dialogue/stream` with `start`, 640-byte PCM frames, `stop`/`cancel`, request IDs and the specified server event family.
- `WebRtcVadState` uses 20 ms WebRTC VAD frames, 3-of-5 speech start, 800 ms silence end, 8 second no-speech timeout, 30 second duration cap and 1 MiB buffer cap.
- Doubao `bigmodel_async` is streamed bidirectionally; partial text only updates subtitles, while normalized final text alone enters RAG/LLM/TTS. Buffered WAV fallback is attempted at most once.
- Android uses `VOICE_COMMUNICATION`, AEC/noise suppression when available, exact 640-byte frames, generation guards, stale socket cancellation and playback interruption on `speech_started`. Missing AEC is surfaced as a release-blocking diagnostic.
- Mock route/VAD tests, full Gateway regression and Android unit/lint/debug assembly pass. A controlled real Doubao call returned three partial events and one final transcript without recording credentials or audio in evidence.
- Android 12 USB/AEC echo behavior and the 9/10 under-700 ms barge-in target remain unverified, so status is `PARTIAL`.
