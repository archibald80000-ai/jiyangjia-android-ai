# Cross-system test matrix

| Layer | Mock | Local real | Cloud real | Physical device |
|---|---:|---:|---:|---:|
| LiveTalking API client | Yes | Yes | Optional | Via Android |
| Wav2Lip rendering | No | GPU required | GPU node | Stream playback |
| Android idle video | N/A | Emulator | N/A | Required |
| USB microphone | Simulated only | N/A | N/A | Required |
| TTS | Mock | Edge | Doubao | Playback required |
| ASR | Mock | Test file | Doubao | USB audio required |
| LLM | Mock | Compatible API | Doubao/Qwen | Indirect |
| Mini FAQ | Yes | Yes | Yes | E2E |
| Network recovery | Simulated | Dev LAN | Internet | Store network |

A milestone cannot be marked production-ready from Mock-only evidence.
