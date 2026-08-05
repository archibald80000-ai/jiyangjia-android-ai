# System architecture

## Logical topology

```text
Android 12 kiosk
  ├─ kiosk UI and state machine
  ├─ USB/default microphone
  ├─ speaker output
  ├─ local idle video
  └─ WebView/WebRTC client
          │ HTTPS / WHEP / WebRTC
          ▼
Gateway on Tencent Cloud (8C/4G/10M)
  ├─ authentication and request IDs
  ├─ ASR adapter
  ├─ mini knowledge + policy
  ├─ LLM adapter
  ├─ TTS adapter
  ├─ session / logs / config
  └─ LiveTalking control adapter
          │ private or protected network
          ▼
GPU node or development PC
  └─ LiveTalking + Wav2Lip/MuseTalk + WebRTC
```

## Responsibilities

### Android

Device interaction, UI state, video/audio playback, microphone selection, local fallback, configuration and telemetry. It contains no cloud API secret.

### Gateway

Business brain and security boundary. It calls ASR/LLM/TTS/knowledge providers, controls answer policy and sends final text/audio/control events to the client or LiveTalking.

### LiveTalking node

Rendering engine. It turns text/audio into a synchronized digital-human stream and exposes WebRTC/WHEP and control endpoints. It must not become the only source of business truth.

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
- One store interaction has a stable `request_id` across Android, gateway, providers and LiveTalking controls.
- Upstream code is pinned and changes are auditable.
