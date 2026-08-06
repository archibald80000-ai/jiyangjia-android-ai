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
from gateway.app.llm import OpenAICompatibleEmbeddingConfig, OpenAICompatibleEmbeddingProvider
from gateway.app.providers import MockEmbeddingProvider
from gateway.app.tts import ProviderCallError, ProviderConfigurationError


def embedding_config_status(provider: str, env_file: str = ".env.local") -> dict[str, object]:
    settings = load_settings(env_file=env_file, override_env_file=True)
    if provider == "mock":
        return {"ok": True, "provider": "mock", "required": {}}
    required = _required_status(provider)
    try:
        config = OpenAICompatibleEmbeddingConfig.from_settings(settings, provider)
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
    parser = argparse.ArgumentParser(description="Test an Embedding provider without printing secrets or full vectors")
    parser.add_argument("--provider", choices=["mock", "doubao", "ark", "openai-compatible"], required=True)
    parser.add_argument("--text", default="")
    parser.add_argument("--env-file", default=".env.local")
    parser.add_argument("--model", default="")
    parser.add_argument("--check-config", action="store_true")
    args = parser.parse_args()

    if args.check_config:
        status = embedding_config_status(args.provider, args.env_file)
        print(json.dumps(status, ensure_ascii=False))
        return 0 if status["ok"] else 2
    if not args.text:
        parser.error("--text is required unless --check-config is used")

    started = time.perf_counter()
    request_id = "manual-embedding-test"
    try:
        if args.provider == "mock":
            result = await MockEmbeddingProvider().embed([args.text], request_id=request_id)
        else:
            settings = load_settings(env_file=args.env_file, override_env_file=True)
            config = OpenAICompatibleEmbeddingConfig.from_settings(settings, args.provider)
            if args.model:
                config = OpenAICompatibleEmbeddingConfig(
                    provider=config.provider,
                    api_key=config.api_key,
                    base_url=config.base_url,
                    model=args.model,
                    timeout_seconds=config.timeout_seconds,
                )
            provider = OpenAICompatibleEmbeddingProvider(config)
            result = await provider.embed([args.text], request_id=request_id)
    except ProviderConfigurationError as exc:
        print(json.dumps({"ok": False, "code": "BLOCKED_PROVIDER_CREDENTIALS", "missing": exc.missing}, ensure_ascii=False))
        return 2
    except ProviderCallError as exc:
        print(json.dumps({"ok": False, "code": exc.code, "retryable": exc.retryable, "message": str(exc)}, ensure_ascii=False))
        return 3 if exc.retryable else 4

    vectors = result["vectors"]
    print(
        json.dumps(
            {
                "ok": True,
                "provider": result["provider"],
                "model_configured": "configured",
                "latency_ms": int((time.perf_counter() - started) * 1000),
                "vector_count": len(vectors),
                "dimensions": result["dimensions"],
                "usage_present": bool(result.get("usage")),
            },
            ensure_ascii=False,
        )
    )
    return 0


def _required_status(provider: str) -> dict[str, str]:
    normalized = provider.lower().strip()
    if normalized in {"doubao", "ark"}:
        return {
            "DOUBAO_EMBEDDING_API_KEY_OR_EMBEDDING_API_KEY_OR_DOUBAO_API_KEY_OR_ARK_API_KEY": "configured"
            if (
                os.environ.get("DOUBAO_EMBEDDING_API_KEY")
                or os.environ.get("EMBEDDING_API_KEY")
                or os.environ.get("DOUBAO_API_KEY")
                or os.environ.get("ARK_API_KEY")
            )
            else "missing",
            "DOUBAO_EMBEDDING_BASE_URL_OR_EMBEDDING_BASE_URL_OR_DOUBAO_BASE_URL_OR_ARK_BASE_URL": "configured"
            if (
                os.environ.get("DOUBAO_EMBEDDING_BASE_URL")
                or os.environ.get("EMBEDDING_BASE_URL")
                or os.environ.get("DOUBAO_BASE_URL")
                or os.environ.get("ARK_BASE_URL")
            )
            else "default",
            "DOUBAO_EMBEDDING_MODEL_OR_EMBEDDING_MODEL": "configured"
            if (os.environ.get("DOUBAO_EMBEDDING_MODEL") or os.environ.get("EMBEDDING_MODEL"))
            else "default",
        }
    return {
        "OPENAI_COMPATIBLE_EMBEDDING_API_KEY_OR_EMBEDDING_API_KEY_OR_OPENAI_COMPATIBLE_API_KEY": "configured"
        if (os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_API_KEY") or os.environ.get("EMBEDDING_API_KEY") or os.environ.get("OPENAI_COMPATIBLE_API_KEY"))
        else "missing",
        "OPENAI_COMPATIBLE_EMBEDDING_BASE_URL_OR_EMBEDDING_BASE_URL_OR_OPENAI_COMPATIBLE_BASE_URL": "configured"
        if (os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_BASE_URL") or os.environ.get("EMBEDDING_BASE_URL") or os.environ.get("OPENAI_COMPATIBLE_BASE_URL"))
        else "missing",
        "OPENAI_COMPATIBLE_EMBEDDING_MODEL_OR_EMBEDDING_MODEL": "configured"
        if (os.environ.get("OPENAI_COMPATIBLE_EMBEDDING_MODEL") or os.environ.get("EMBEDDING_MODEL"))
        else "missing",
    }


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
