from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.asr import DoubaoASRConfig, DoubaoASRProvider
from gateway.app.config import load_settings
from gateway.app.providers import MockASRProvider
from gateway.app.tts import ProviderCallError, ProviderConfigurationError


def doubao_asr_config_status(env_file: str = ".env.local") -> dict[str, object]:
    settings = load_settings(env_file=env_file, override_env_file=True)
    required_status = {
        "DOUBAO_ASR_APP_ID": "configured" if (os.environ.get("DOUBAO_ASR_APP_ID") or os.environ.get("DOUBAO_REALTIME_APP_ID")) else "missing",
        "DOUBAO_ASR_ACCESS_TOKEN": "configured"
        if (
            os.environ.get("DOUBAO_ASR_ACCESS_TOKEN")
            or os.environ.get("DOUBAO_ASR_TOKEN")
            or os.environ.get("DOUBAO_ASR_KEY")
            or os.environ.get("DOUBAO_REALTIME_ACCESS_TOKEN")
        )
        else "missing",
        "DOUBAO_ASR_API_KEY": "configured" if os.environ.get("DOUBAO_ASR_API_KEY") else "missing",
        "DOUBAO_ASR_RESOURCE_ID": "configured" if os.environ.get("DOUBAO_ASR_RESOURCE_ID") else "default",
    }
    try:
        DoubaoASRConfig.from_settings(settings)
    except ProviderConfigurationError:
        return {
            "ok": False,
            "code": "BLOCKED_PROVIDER_CREDENTIALS",
            "provider": "doubao",
            "required": required_status,
            "auth_note": "configure DOUBAO_ASR_API_KEY or DOUBAO_ASR_APP_ID plus DOUBAO_ASR_ACCESS_TOKEN; DOUBAO_REALTIME_APP_ID/ACCESS_TOKEN are accepted as compatibility aliases",
        }
    return {"ok": True, "provider": "doubao", "required": required_status}


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test an ASR provider without printing secrets")
    parser.add_argument("--provider", choices=["mock", "doubao"], required=True)
    parser.add_argument("--file", default="")
    parser.add_argument("--content-type", default="")
    parser.add_argument("--env-file", default=".env.local")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    if args.check_config:
        if args.provider == "mock":
            print(json.dumps({"ok": True, "provider": "mock", "required": {}}, ensure_ascii=False))
            return 0
        status = doubao_asr_config_status(args.env_file)
        print(json.dumps(status, ensure_ascii=False))
        return 0 if status["ok"] else 2

    if not args.file:
        parser.error("--file is required unless --check-config is used")
    audio_path = Path(args.file)
    audio = audio_path.read_bytes()
    content_type = args.content_type or mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
    request_id = "manual-asr-test"
    try:
        if args.provider == "mock":
            result = await MockASRProvider().transcribe(audio, content_type, request_id=request_id)
        else:
            settings = load_settings(env_file=args.env_file, override_env_file=True)
            result = await DoubaoASRProvider(DoubaoASRConfig.from_settings(settings)).transcribe(audio, content_type, request_id=request_id)
    except ProviderConfigurationError as exc:
        print(json.dumps({"ok": False, "code": "BLOCKED_PROVIDER_CREDENTIALS", "missing": exc.missing}, ensure_ascii=False))
        return 2
    except ProviderCallError as exc:
        print(json.dumps({"ok": False, "code": exc.code, "retryable": exc.retryable, "message": str(exc)}, ensure_ascii=False))
        return 3 if exc.retryable else 4

    print(
        json.dumps(
            {
                "ok": True,
                "provider": result["provider"],
                "content_type": content_type,
                "bytes": len(audio),
                "sha256": hashlib.sha256(audio).hexdigest().upper(),
                "text": result["text"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
