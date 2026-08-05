# Observability

## Correlation

Generate one `request_id` for every interaction and propagate it across Android, gateway, providers and LiveTalking controls.

## Minimum events

- App start/version/device ID.
- Network and selected audio devices.
- Recording start/end and byte duration (not raw content by default).
- ASR, knowledge/LLM, TTS and LiveTalking timings.
- Playback start/end.
- State transitions.
- Error code, retry and fallback.

## Sensitive logging

Never log tokens, full credentials, raw provider authorization headers or unrestricted personal transcripts. Apply masking and retention limits.

## Pilot dashboard questions

- Is the app online?
- Which microphone is selected?
- Which display mode is active?
- What is the last successful interaction?
- Where is latency spent?
- How often does fallback occur?
- Which errors require staff action?
