# Product requirements

## 1. Goal

Provide a store-facing Android 12 AI voice service terminal that can receive customer speech through a USB microphone, generate a controlled answer, play the answer through speakers, display subtitles/status and show a local idle character video. LiveTalking digital-human rendering is a future enhancement, not a Phase 1 dependency.

## 2. Primary user journey

```text
Android starts
→ local idle character video loops
→ customer taps start
→ Android records USB/default microphone audio
→ gateway performs Doubao ASR
→ mini FAQ / LLM generates controlled answer
→ Doubao TTS creates speech
→ Android plays audio and subtitles
→ return to idle
```

## 3. V1 functional requirements

- Landscape immersive Android APK.
- Local idle video loop with no network dependency.
- USB microphone preference and default-input fallback.
- Built-in or external speaker playback.
- Configurable server address and `idle_video_voice` display mode.
- Network error, timeout, reconnect and recoverable states.
- Provider adapters for Mock, Doubao ASR/TTS and configurable LLMs.
- 10–30 reviewed mini FAQ entries with prohibited-topic and transfer rules.
- Request IDs, structured logs, basic health/status reporting.

## 4. Explicit non-goals for early phases

- Full enterprise knowledge-management platform.
- Vector database or automatic ingestion of `E:\work\积养家`.
- Local LLM on Android or the 4 GB cloud server.
- Production-grade multi-tenant administration.
- Real-time 3D skeleton/gesture control.
- LiveTalking, Wav2Lip, MuseTalk, WebRTC digital human, multi-stream concurrency, RTMP live commerce and advanced voice cloning in Phase 1.

## 5. Experience targets

- The customer always sees a stable avatar or idle video.
- A provider or network failure produces a friendly message and fallback, not a blank screen.
- Speech answers are short, conversational and normally 50–150 Chinese characters.
- Medical diagnosis, treatment claims, uncertain prices and unsupported facts transfer to staff.

## 6. Success metrics for pilot

- 30 consecutive test conversations without app crash.
- USB microphone correctly selected or safe fallback recorded.
- Network disconnect/reconnect recovers without reinstalling the APK.
- P95 end-to-end response target measured and reported; no invented target claims before evidence.
- At least 90% of curated FAQ test questions return an approved answer or safe transfer.
