# ADR-0001: Android client with remote services

- Status: Accepted
- Date: 2026-08-05

## Decision

Use an Android 12 APK as the device client. Run ASR/LLM/TTS/gateway and LiveTalking on remote or local-computer services, not inside the Android device.

## Reason

The display is Android, cannot run Windows EXE/CUDA/Python GPU inference reliably, and should remain a thin recoverable kiosk.
