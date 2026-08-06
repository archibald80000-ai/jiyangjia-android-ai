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


def doubao_tts_config_status() -> dict[str, object]:
    settings = load_settings()
    try:
        DoubaoTTSConfig.from_settings(settings)
    except ProviderConfigurationError as exc:
        required = ["DOUBAO_TTS_APP_ID", "DOUBAO_TTS_ACCESS_TOKEN", "DOUBAO_TTS_VOICE_TYPE"]
        return {
            "ok": False,
            "code": "BLOCKED_PROVIDER_CREDENTIALS",
            "provider": "doubao",
            "required": {name: "missing" if name in exc.missing else "configured" for name in required},
        }
    return {
        "ok": True,
        "provider": "doubao",
        "required": {
            "DOUBAO_TTS_APP_ID": "configured",
            "DOUBAO_TTS_ACCESS_TOKEN": "configured",
            "DOUBAO_TTS_VOICE_TYPE": "configured",
        },
    }


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test a TTS provider without printing secrets")
    parser.add_argument("--provider", choices=["mock", "doubao"], required=True)
    parser.add_argument("--text", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    if args.check_config:
        if args.provider == "mock":
            print(json.dumps({"ok": True, "provider": "mock", "required": {}}, ensure_ascii=False))
            return 0
        status = doubao_tts_config_status()
        print(json.dumps(status, ensure_ascii=False))
        return 0 if status["ok"] else 2

    if not args.text:
        parser.error("--text is required unless --check-config is used")

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
