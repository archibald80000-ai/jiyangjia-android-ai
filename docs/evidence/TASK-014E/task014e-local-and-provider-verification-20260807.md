# TASK-014E verification — 2026-08-07

## Local automated results

- `python -m pytest tests/asr/test_streaming_asr.py tests/gateway/test_gateway_api.py -q`: 10 passed.
- `python -m pytest tests -q`: 61 passed, one pre-existing FAISS/NumPy deprecation warning.
- Android `gradlew.bat testDebugUnitTest lintDebug assembleDebug`: `BUILD SUCCESSFUL`, 51 actionable tasks.
- No raw PCM, WAV, provider packet, token or credential was retained in this evidence directory.

## Controlled Doubao bidirectional stream

Input was a temporary, ignored 16 kHz mono PCM16 conversion of a generated phrase. The temporary audio is not tracked.

```json
{"ok":true,"provider":"doubao","partial_events":3,"text":"您好，欢迎来到鸡养家。"}
```

The provider emitted partial text while audio frames were still being sent and one final transcript. The final homophone is handled by the existing final-only brand normalizer; partial events never invoke retrieval or answer generation.

## Unverified release gates

- No Android 12 device was connected, so AEC availability, USB routing, speaker echo false positives and `speech_started`-to-stop latency are not claimed.
- The required 9/10 interruption success and 0/10 playback-only false-trigger criteria remain TASK-015 gates.
- Status remains `PARTIAL`.
