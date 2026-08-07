from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys
import wave

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.asr import DoubaoASRConfig, DoubaoASRProvider
from gateway.app.config import load_settings
from gateway.app.streaming_asr import DoubaoStreamingASRProvider, FRAME_BYTES
from gateway.app.tts import ProviderCallError, ProviderConfigurationError


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test Doubao bidirectional streaming ASR without logging audio or credentials")
    parser.add_argument("--file", required=True, help="16 kHz mono PCM16 WAV")
    parser.add_argument("--env-file", default=".env.local")
    args = parser.parse_args()
    try:
        settings = load_settings(args.env_file, override_env_file=True)
        provider = DoubaoASRProvider(DoubaoASRConfig.from_settings(settings))
        streaming = DoubaoStreamingASRProvider(provider, settings.doubao_streaming_asr_endpoint)
        with wave.open(args.file, "rb") as source:
            if (source.getframerate(), source.getnchannels(), source.getsampwidth()) != (16_000, 1, 2):
                raise ValueError("input must be 16 kHz mono PCM16 WAV")
            pcm = source.readframes(source.getnframes())
        session = await streaming.open_stream("manual-streaming-asr-test")
        partials: list[str] = []
        try:
            for offset in range(0, len(pcm), FRAME_BYTES):
                frame = pcm[offset : offset + FRAME_BYTES]
                if len(frame) < FRAME_BYTES:
                    frame += bytes(FRAME_BYTES - len(frame))
                partials.extend(await session.push(frame))
                await asyncio.sleep(0.02)
            result = await session.finish()
        finally:
            await session.close()
    except ProviderConfigurationError as exc:
        print(json.dumps({"ok": False, "code": "BLOCKED_PROVIDER_CREDENTIALS", "missing": exc.missing}, ensure_ascii=False))
        return 2
    except (ProviderCallError, ValueError) as exc:
        print(json.dumps({"ok": False, "code": getattr(exc, "code", "INVALID_AUDIO"), "message": str(exc)}, ensure_ascii=False))
        return 3
    print(json.dumps({"ok": True, "provider": "doubao", "partial_events": len(partials), "text": result["text"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
