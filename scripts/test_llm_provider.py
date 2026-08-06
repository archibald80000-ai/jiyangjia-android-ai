from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.config import load_settings
from gateway.app.llm import OpenAICompatibleChatConfig, OpenAICompatibleLLMProvider
from gateway.app.providers import MockLLMProvider
from gateway.app.tts import ProviderCallError, ProviderConfigurationError


def llm_config_status(provider: str, env_file: str = ".env.local") -> dict[str, object]:
    settings = load_settings(env_file=env_file, override_env_file=True)
    if provider == "mock":
        return {"ok": True, "provider": "mock", "required": {}}
    required = _required_status(provider, embedding=False)
    try:
        config = OpenAICompatibleChatConfig.from_settings(settings, provider)
    except ProviderConfigurationError as exc:
        return {
            "ok": False,
            "code": "BLOCKED_PROVIDER_CREDENTIALS",
            "provider": provider,
            "required": required,
            "missing": exc.missing,
        }
    return {
        "ok": True,
        "provider": config.provider,
        "required": required,
        "model_configured": "configured" if config.model else "missing",
        "base_url_configured": "configured" if config.base_url else "missing",
    }


async def main() -> int:
    parser = argparse.ArgumentParser(description="Test an LLM provider without printing secrets")
    parser.add_argument("--provider", choices=["mock", "deepseek", "doubao", "ark", "openai-compatible"], required=True)
    parser.add_argument("--prompt", default="")
    parser.add_argument("--env-file", default=".env.local")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    if args.check_config:
        status = llm_config_status(args.provider, args.env_file)
        print(json.dumps(status, ensure_ascii=False))
        return 0 if status["ok"] else 2
    if not args.prompt:
        parser.error("--prompt is required unless --check-config is used")

    started = time.perf_counter()
    request_id = "manual-llm-test"
    try:
        if args.provider == "mock":
            result = await MockLLMProvider().chat([{"role": "user", "content": args.prompt}], [], request_id=request_id)
        else:
            settings = load_settings(env_file=args.env_file, override_env_file=True)
            provider = OpenAICompatibleLLMProvider(OpenAICompatibleChatConfig.from_settings(settings, args.provider))
            result = await provider.chat([{"role": "user", "content": args.prompt}], [], request_id=request_id)
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
                "model_configured": "configured",
                "latency_ms": int((time.perf_counter() - started) * 1000),
                "text": result["text"],
                "usage_present": bool(result.get("usage")),
            },
            ensure_ascii=False,
        )
    )
    return 0


def _required_status(provider: str, *, embedding: bool) -> dict[str, str]:
    del embedding
    normalized = provider.lower().strip()
    if normalized == "deepseek":
        return {
            "DEEPSEEK_API_KEY": "configured" if os.environ.get("DEEPSEEK_API_KEY") else "missing",
            "DEEPSEEK_BASE_URL": "configured" if os.environ.get("DEEPSEEK_BASE_URL") else "default",
            "DEEPSEEK_MODEL": "configured" if os.environ.get("DEEPSEEK_MODEL") else "default",
        }
    if normalized in {"doubao", "ark"}:
        return {
            "DOUBAO_API_KEY_OR_ARK_API_KEY": "configured" if (os.environ.get("DOUBAO_API_KEY") or os.environ.get("ARK_API_KEY")) else "missing",
            "DOUBAO_BASE_URL_OR_ARK_BASE_URL": "configured" if (os.environ.get("DOUBAO_BASE_URL") or os.environ.get("ARK_BASE_URL")) else "default",
            "DOUBAO_MODEL_OR_ARK_MODEL": "configured" if (os.environ.get("DOUBAO_MODEL") or os.environ.get("ARK_MODEL")) else "missing",
        }
    return {
        "OPENAI_COMPATIBLE_API_KEY": "configured" if os.environ.get("OPENAI_COMPATIBLE_API_KEY") else "missing",
        "OPENAI_COMPATIBLE_BASE_URL": "configured" if os.environ.get("OPENAI_COMPATIBLE_BASE_URL") else "missing",
        "OPENAI_COMPATIBLE_MODEL": "configured" if os.environ.get("OPENAI_COMPATIBLE_MODEL") else "missing",
    }


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
