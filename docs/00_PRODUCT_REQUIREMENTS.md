# Product requirements

## 1. Goal

Provide a store-facing Android 12 AI voice service terminal that can receive customer speech through a USB microphone, generate a controlled answer, play the answer through speakers, display subtitles/status and optionally render a speaking digital person through LiveTalking.

## 2. Primary user journey

```text
Idle avatar/video
→ customer starts speaking
→ Android records or streams audio
→ gateway performs ASR
→ mini knowledge / LLM generates controlled answer
→ TTS creates speech
→ idle-video playback or LiveTalking rendering
→ answer ends
→ return to idle
```

## 3. V1 functional requirements

- Landscape immersive Android APK.
- Local idle video loop with no network dependency.
- USB microphone preference and default-input fallback.
- Built-in or external speaker playback.
- Configurable server address and display mode.
- Network error, timeout, reconnect and recoverable states.
- LiveTalking WebRTC/WHEP playback when available.
- Text and audio drive, interrupt and status integration.
- Provider adapters for Mock, EdgeTTS, Doubao ASR/TTS and LLMs.
- 10–30 reviewed mini FAQ entries with prohibited-topic and transfer rules.
- Request IDs, structured logs, basic health/status reporting.

## 4. Explicit non-goals for early phases

- Full enterprise knowledge-management platform.
- Vector database or automatic ingestion of `E:\work\积养家`.
- Local LLM on Android or the 4 GB cloud server.
- Production-grade multi-tenant administration.
- Real-time 3D skeleton/gesture control.
- MuseTalk, multi-stream concurrency, RTMP live commerce and advanced voice cloning before Wav2Lip baseline passes.

## 5. Experience targets

- The customer always sees a stable avatar or idle video.
- A provider or GPU failure produces a friendly message and fallback, not a blank screen.
- Speech answers are short, conversational and normally 50–150 Chinese characters.
- Medical diagnosis, treatment claims, uncertain prices and unsupported facts transfer to staff.

## 6. Success metrics for pilot

- 30 consecutive test conversations without app crash.
- USB microphone correctly selected or safe fallback recorded.
- Network disconnect/reconnect recovers without reinstalling the APK.
- P95 end-to-end response target measured and reported; no invented target claims before evidence.
- At least 90% of curated FAQ test questions return an approved answer or safe transfer.
