# Core facts

## Product

- Door/store digital service terminal for Jiyangjia.
- Android 12 large display is the primary client.
- Interaction target: USB microphone input, AI answer, speaker output, subtitles/status and avatar display.
- Phase 1 prioritizes local idle character video, tap-to-talk voice FAQ, subtitles and reliable fallback over photorealistic rendering.

## Infrastructure

- Local workspace: `E:\work\ai-kefu\jiyangjia-ai`.
- Raw business materials: `E:\work\积养家` and remain read-only until a curated task is approved.
- Existing cloud: Tencent Cloud 8 vCPU / 4 GB RAM / 10 Mbps / no GPU.
- Real-time LiveTalking inference is deferred and would require a separate compatible GPU node or development PC.

## Architecture

- Android client never stores provider secrets.
- Gateway owns ASR/LLM/TTS/knowledge calls, sessions, policy and logs.
- LiveTalking is an upstream rendering engine integrated by API, not the business brain.
- Phase 1 display mode is `idle_video_voice`; future `livetalking_webrtc` remains an extension point.
- Initial knowledge is lightweight RAG: reviewed Markdown/TXT/PDF/DOCX documents, SQLite metadata, local FAISS index, embedding provider adapter, Top-K retrieval and source citations.

## Quality

- A feature is not complete without reproducible tests and evidence.
- Mock results must be labelled Mock.
- Real API completion requires real Doubao ASR/TTS, Volcengine Ark or OpenAI-compatible LLM and embedding evidence; missing credentials are blockers, not success.
- Public repository contains no private source documents, model weights, avatar rights-sensitive assets or secrets.
