# System architecture

## Logical topology

```text
Android 12 kiosk
  ├─ kiosk UI and state machine
  ├─ USB/default microphone
  ├─ speaker output
  ├─ local idle video
  └─ subtitles/status
          │ HTTPS
          ▼
Gateway on Tencent Cloud (8C/4G/10M)
  ├─ authentication and request IDs
  ├─ ASR adapter
  ├─ mini knowledge + policy
  ├─ LLM adapter
  ├─ TTS adapter
  ├─ session / logs / config
  └─ future LiveTalking adapter boundary
```

## Responsibilities

### Android

Device interaction, UI state, video/audio playback, microphone selection, local fallback, configuration and telemetry. It contains no cloud API secret.

### Gateway

Business brain and security boundary. It calls ASR/LLM/TTS/knowledge providers, controls answer policy and sends final text/audio/subtitle events to the client.

### LiveTalking node

Deferred rendering engine. It may later turn text/audio into a synchronized digital-human stream and expose WebRTC/WHEP and control endpoints, but it is not part of Phase 1 and must not become the only source of business truth.

## State machine

```text
INITIALIZING
  → IDLE
  → LISTENING
  → RECOGNIZING
  → THINKING
  → SPEAKING
  → IDLE

Any active state
  → NETWORK_ERROR | DEVICE_ERROR | SERVER_ERROR
  → fallback/retry
  → IDLE
```

## Key architecture invariants

- `idle_video` works without LiveTalking.
- Provider adapters can be swapped by configuration.
- Raw recordings are not retained by default.
- One store interaction has a stable `request_id` across Android, gateway and providers.
- Upstream code is pinned and changes are auditable.

Phase 1 detailed architecture is in `architecture/MVP_ARCHITECTURE.md`.
