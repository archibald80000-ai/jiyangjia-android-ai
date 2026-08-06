# Future LiveTalking Upgrade

Updated: 2026-08-06

## Status

LiveTalking, Wav2Lip, MuseTalk, realtime lip sync, WebRTC digital human mode and GPU inference are deferred from Phase 1.

Existing LiveTalking documentation, scripts, evidence and upstream checkout are retained for future use. They must not block the Android + Gateway voice FAQ MVP.

## Deferred Items

- `wav2lip256.pth`
- `s3fd.pth`
- `wav2lip256_avatar1.zip`
- LiveTalking realtime inference
- Wav2Lip/MuseTalk model evaluation
- WebRTC digital-human mode
- GPU node deployment

## Future Integration Boundary

The MVP keeps these extension points:

- Android `DisplayMode`: `idle_video_voice` in Phase 1, `livetalking_webrtc` later.
- Gateway dialogue result shape includes `answer_text`, `answer_audio`, `display_actions`.
- A future `AvatarRenderer` adapter can send text/audio to LiveTalking `/human` or `/humanaudio`.
- Android can add a WebView/WebRTC scene without changing ASR/LLM/TTS/FAQ contracts.

## Future Preconditions

LiveTalking work can resume only after:

- Phase 1 voice FAQ loop is accepted on Android 12 device;
- model/avatar assets and rights are available;
- GPU runtime is available and justified;
- WebRTC/TURN/network requirements are approved;
- rollback to idle video remains available.

## Upgrade Path

1. Re-open deferred TASK-003/TASK-004 or create a new enhancement task set.
2. Prepare official assets outside Git.
3. Verify LiveTalking local startup, WebRTC/WHEP, `/human`, `/humanaudio`, interrupt and FPS.
4. Add Android `livetalking_webrtc` display mode behind config.
5. Run A/B acceptance against `idle_video_voice` fallback.
