# Deployment topology

## Development

```text
Windows development PC
  ├─ Gateway
  ├─ Android emulator / ADB device
  └─ LiveTalking if compatible NVIDIA GPU exists
```

## Pilot

```text
Android 12 store screen
  │ HTTPS/WebRTC
  ├──────────────► Tencent Cloud gateway (observed 2 CPU cores / about 1.9Gi RAM / 10M)
  │                         │
  │                         └─ cloud ASR/LLM/TTS
  │
  └──────────────► GPU node / dev PC LiveTalking (optional)
```

## Resource policy

The current small CPU-only server should run a small gateway, reverse proxy, lightweight database and logs. Heavy document parsing, local LLMs, vector stacks and LiveTalking inference are out of scope for that machine.

## Production prerequisites

- Domain and TLS.
- Firewall/security-group rules.
- Authenticated device and admin routes.
- TURN strategy if direct WebRTC cannot traverse networks.
- Monitoring, backup, log rotation and rollback.
- Measured bandwidth for actual video resolution and concurrency.
