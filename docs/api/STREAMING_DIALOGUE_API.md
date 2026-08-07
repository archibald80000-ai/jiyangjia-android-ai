# Streaming Dialogue API

- Status: Draft for TASK-014E
- Transport: WebSocket over TLS (`wss://`)
- Path: `/api/v1/dialogue/stream`

## Client Events

JSON control frames:

- `start`: `request_id`, `session_id`, `device_id`, sample rate, channels and PCM format;
- `stop`: finish the utterance and request final recognition;
- `cancel`: invalidate the session and suppress later answer/audio events.

Binary frames contain mono PCM audio. The initial implementation uses 16 kHz, signed 16-bit little-endian frames of 20 to 100 milliseconds.

## Server Events

- `ready`: stream accepted;
- `speech_started`: VAD detected speech;
- `partial_transcript`: non-final text for subtitles;
- `speech_ended`: VAD end-of-utterance;
- `final_transcript`: normalized final text plus optional `raw_text`;
- `stage`: `rag`, `llm` or `tts` progress;
- `answer`: answer text, subtitles and sources;
- `tts_ready`: `audio_id`, content type, size and duration when known;
- `error`: `request_id`, code, `failed_stage`, user message and retryable flag.

Every event includes `request_id`. Provider credentials and raw authorization failures are never returned.

## Session Rules

- Only one active capture stream is allowed per Android consultation session.
- A newly started stream cancels prior playback/response delivery for that session.
- Partial transcript events are not sent to RAG or LLM.
- Brand normalization and knowledge processing run only after final transcript.
- WebSocket or streaming Provider failure falls back to the existing multipart WAV dialogue path when buffered audio is still available.
- Idle timeout, maximum utterance duration, maximum bytes and per-device rate limits are mandatory.

## Acceptance

- Real speech produces at least one partial event before the final event.
- VAD terminates a normal utterance without a second tap.
- Final transcript continues through RAG, LLM and TTS with sources and audio retrieval.
- Tap during playback stops old audio and begins a new request without playing the stale answer later.
- Disconnect and Provider failures return a stage-specific error and preserve WAV fallback.
