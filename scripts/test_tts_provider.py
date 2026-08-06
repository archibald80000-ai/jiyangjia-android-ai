from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.config import load_settings
from gateway.app.providers import MockTTSProvider
from gateway.app.tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderConfigurationError


def doubao_tts_config_status(env_file: str = ".env.local") -> dict[str, object]:
    settings = load_settings(env_file=env_file, override_env_file=True)
    required_status = {
        "DOUBAO_TTS_APP_ID": "configured" if os.environ.get("DOUBAO_TTS_APP_ID") else "missing",
        "DOUBAO_TTS_ACCESS_TOKEN": "configured" if os.environ.get("DOUBAO_TTS_ACCESS_TOKEN") else "missing",
        "DOUBAO_TTS_API_KEY": "configured" if os.environ.get("DOUBAO_TTS_API_KEY") else "missing",
        "DOUBAO_TTS_SPEAKER": "configured" if (os.environ.get("DOUBAO_TTS_SPEAKER") or os.environ.get("DOUBAO_TTS_VOICE_TYPE")) else "missing",
        "DOUBAO_TTS_RESOURCE_ID": "configured" if os.environ.get("DOUBAO_TTS_RESOURCE_ID") else "missing",
    }
    try:
        DoubaoTTSConfig.from_settings(settings)
    except ProviderConfigurationError as exc:
        return {
            "ok": False,
            "code": "BLOCKED_PROVIDER_CREDENTIALS",
            "provider": "doubao",
            "required": required_status,
            "auth_note": "configure DOUBAO_TTS_API_KEY or DOUBAO_TTS_APP_ID plus DOUBAO_TTS_ACCESS_TOKEN",
        }
    return {
        "ok": True,
        "provider": "doubao",
        "required": required_status,
    }


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test a TTS provider without printing secrets")
    parser.add_argument("--provider", choices=["mock", "doubao"], required=True)
    parser.add_argument("--text", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--check-config", action="store_true")
    parser.add_argument("--env-file", default=".env.local")
    args = parser.parse_args()

    if args.check_config:
        if args.provider == "mock":
            print(json.dumps({"ok": True, "provider": "mock", "required": {}}, ensure_ascii=False))
            return 0
        status = doubao_tts_config_status(args.env_file)
        print(json.dumps(status, ensure_ascii=False))
        return 0 if status["ok"] else 2

    if not args.text:
        parser.error("--text is required unless --check-config is used")

    if args.provider == "mock":
        result = await MockTTSProvider().synthesize(args.text, voice_id=None, request_id="manual-tts-test")
    else:
        try:
            settings = load_settings(env_file=args.env_file, override_env_file=True)
            result = await DoubaoTTSProvider(DoubaoTTSConfig.from_settings(settings)).synthesize(
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
