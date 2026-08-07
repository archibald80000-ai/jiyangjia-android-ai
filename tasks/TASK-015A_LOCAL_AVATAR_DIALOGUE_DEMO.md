# TASK-015A - Local Avatar Dialogue Demo

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-014C through TASK-014G local implementation, user-approved portrait source media
- **Scope:** local runtime media preparation, local asset/Profile publication, browser kiosk demo, tests and evidence

## Goal

Use the explicitly approved `E:\work\ai-kefu\资料库\人像背景.MOV` as a local 9:16 idle-avatar source and demonstrate the existing ASR/RAG/LLM/TTS dialogue over the published video, background, subtitles and Profile.

## Acceptance

- Source MOV remains unchanged.
- Runtime MP4 is H.264, 1080x1920, 30 fps, yuv420p and silent.
- A same-source 1080x1920 JPG background is published.
- Both assets are published and bound to the default portrait Profile.
- `/demo/kiosk` loads manifest/Profile and supports microphone plus text dialogue.
- Dialogue returns request ID, answer, sources when matched, TTS audio ID and playable audio.
- Runtime media and recordings are not committed to Git.

## Boundary

This is an idle-video voice avatar demonstration, not LiveTalking, lip sync or real-time rendered facial animation. Android physical acceptance remains blocked until a device is connected.

## Result (2026-08-07)

- The source MOV remained unchanged and the user confirmed its usage rights for this project.
- Ignored runtime outputs were prepared as H.264 1080x1920 MP4 and same-source JPG background.
- Both assets were uploaded, published, downloaded back with matching SHA-256 values, and bound to `display-1080x1920`.
- The final local Profile is portrait 1080x1920, `fit`, subtitle font 36 px, subtitle bottom safe area 16%, and consult button at `(0.5, 0.9)`.
- `/demo/kiosk` was verified in a 9:16 browser viewport with a decoded looping video, real RAG source, request ID, generated subtitle and playable Doubao TTS.
- The consultation button now supports both manual `结束并发送` and automatic upload after speech has been detected followed by 3 seconds of silence. No-speech startup does not upload an empty recording; the configured maximum duration remains the fallback.
- Browser microphone capture is implemented but remains a manual acceptance item because the user must grant microphone permission. Android physical acceptance remains blocked.

Evidence: `docs/evidence/TASK-015A/local-avatar-dialogue-demo-20260807.md`.
