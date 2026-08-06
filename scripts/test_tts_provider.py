from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.config import load_settings
from gateway.app.providers import MockTTSProvider
from gateway.app.tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderConfigurationError


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test a TTS provider without printing secrets")
    parser.add_argument("--provider", choices=["mock", "doubao"], required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    if args.provider == "mock":
        result = await MockTTSProvider().synthesize(args.text, voice_id=None, request_id="manual-tts-test")
    else:
        try:
            result = await DoubaoTTSProvider(DoubaoTTSConfig.from_settings(load_settings())).synthesize(
                args.text,
                voice_id=None,
                request_id="manual-tts-test",
            )
        except ProviderConfigurationError as exc:
            print(json.dumps({"ok": False, "code": "BLOCKED_PROVIDER_CREDENTIALS", "missing": exc.missing}, ensure_ascii=False))
            return 2

    audio = bytes(result["content"])
    if args.output:
        Path(args.output).write_bytes(audio)
    print(
        json.dumps(
            {
                "ok": True,
                "provider": result["provider"],
                "content_type": result["content_type"],
                "bytes": len(audio),
                "sha256": hashlib.sha256(audio).hexdigest().upper(),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
