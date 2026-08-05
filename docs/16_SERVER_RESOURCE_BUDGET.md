# Tencent Cloud resource budget

Known server: 8 vCPU, 4 GB RAM, 10 Mbps, no GPU.

## Appropriate early workloads

- Nginx/reverse proxy.
- Lightweight FastAPI gateway.
- SQLite or carefully configured small PostgreSQL instance.
- Session/configuration and compact structured logs.
- Calls to external ASR/LLM/TTS APIs.
- Mini FAQ data.

## Inappropriate workloads

- LiveTalking Wav2Lip/MuseTalk inference.
- Local LLM.
- Large Dify/vector/database stack without resource measurement.
- High-bitrate multi-stream video relay by default.
- Unbounded file parsing or retained audio.

## Required measurements

Codex must record idle and loaded memory, CPU, disk, request concurrency and network before recommending production readiness or an upgrade.
