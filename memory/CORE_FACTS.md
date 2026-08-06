# Core facts

## Product

- Door/store digital service terminal for Jiyangjia.
- Android 12 large display is the primary client.
- Interaction target: USB microphone input, AI answer, speaker output, subtitles/status and avatar display.
- V1 prioritizes reliability and understandable fallback over photorealistic rendering.

## Infrastructure

- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`.
- Raw business materials: `E:\work\积养家` and remain read-only until a curated task is approved.
- Existing cloud: Tencent Cloud 8 vCPU / 4 GB RAM / 10 Mbps / no GPU.
- Real-time LiveTalking inference requires a separate compatible GPU node or development PC.

## Architecture

- Android client never stores provider secrets.
- Gateway owns ASR/LLM/TTS/knowledge calls, sessions, policy and logs.
- LiveTalking is an upstream rendering engine integrated by API, not the business brain.
- Dual display mode is mandatory: `idle_video` and `livetalking_webrtc`.
- Initial knowledge is a small reviewed FAQ, not a full vector knowledge base.

## Quality

- A feature is not complete without reproducible tests and evidence.
- Mock results must be labelled Mock.
- Public repository contains no private source documents, model weights, avatar rights-sensitive assets or secrets.
