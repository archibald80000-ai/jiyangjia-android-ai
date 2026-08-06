from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_ENV_FILE = "secrets/.env.local"
EXPECTED_COMPOSE_ENV_FILE = "../secrets/.env.local"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check provider env readiness without printing secret values.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE)
    parser.add_argument("--compose-file", default="deploy/docker-compose.yml")
    parser.add_argument("--require-real-mvp", action="store_true")
    args = parser.parse_args()

    env_path = Path(args.env_file)
    env = _parse_env_file(env_path)
    provider_checks = _provider_checks(env)
    real_mvp_ready = all(
        provider_checks[name]["ready"] and provider_checks[name]["provider"] != "mock"
        for name in ("asr", "tts", "llm", "embedding")
    )
    payload = {
        "ok": real_mvp_ready if args.require_real_mvp else True,
        "env_file": _env_file_status(env_path),
        "compose": _compose_status(Path(args.compose_file)),
        "providers": provider_checks,
        "real_mvp_ready": real_mvp_ready,
        "next_action": "run_dialogue_acceptance" if real_mvp_ready else "fix_provider_env_chain",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 2


def _parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def _env_file_status(path: Path) -> dict[str, Any]:
    status: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "readable": os.access(path, os.R_OK) if path.exists() else False,
    }
    if path.exists():
        try:
            status["mode"] = oct(path.stat().st_mode & 0o777)
        except OSError:
            status["mode"] = "unknown"
    return status


def _compose_status(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return {
        "path": str(path),
        "exists": path.exists(),
        "expected_env_file": EXPECTED_COMPOSE_ENV_FILE,
        "points_to_expected_env_file": EXPECTED_COMPOSE_ENV_FILE in text,
        "contains_old_root_env_file": "../.env.local" in text,
    }


def _provider_checks(env: dict[str, str]) -> dict[str, dict[str, Any]]:
    return {
        "asr": _check_asr(env),
        "tts": _check_tts(env),
        "llm": _check_llm(env),
        "embedding": _check_embedding(env),
    }


def _check_asr(env: dict[str, str]) -> dict[str, Any]:
    provider = _value(env, "JIYANGJIA_ASR_PROVIDER", "mock")
    if provider != "doubao":
        return _mock_or_unsupported(provider, "doubao")
    has_api_key = _has_any(env, "DOUBAO_ASR_API_KEY")
    has_app_token = _has_any(env, "DOUBAO_ASR_APP_ID", "DOUBAO_REALTIME_APP_ID") and _has_any(
        env,
        "DOUBAO_ASR_ACCESS_TOKEN",
        "DOUBAO_ASR_TOKEN",
        "DOUBAO_ASR_KEY",
        "DOUBAO_REALTIME_ACCESS_TOKEN",
    )
    missing = []
    if not (has_api_key or has_app_token):
        missing.append("DOUBAO_ASR_AUTH")
    return _provider_result(provider, missing)


def _check_tts(env: dict[str, str]) -> dict[str, Any]:
    provider = _value(env, "JIYANGJIA_TTS_PROVIDER", "mock")
    if provider != "doubao":
        return _mock_or_unsupported(provider, "doubao")
    has_api_key = _has_any(env, "DOUBAO_TTS_API_KEY")
    has_app_token = _has_any(env, "DOUBAO_TTS_APP_ID") and _has_any(
        env,
        "DOUBAO_TTS_ACCESS_TOKEN",
        "DOUBAO_TTS_TOKEN",
        "DOUBAO_TTS_KEY",
    )
    missing = []
    if not (has_api_key or has_app_token):
        missing.append("DOUBAO_TTS_AUTH")
    if not _has_any(env, "DOUBAO_TTS_SPEAKER", "DOUBAO_TTS_VOICE_TYPE"):
        missing.append("DOUBAO_TTS_SPEAKER")
    return _provider_result(provider, missing)


def _check_llm(env: dict[str, str]) -> dict[str, Any]:
    provider = _value(env, "JIYANGJIA_LLM_PROVIDER", "mock")
    if provider in {"doubao", "ark", "volcengine"}:
        missing = []
        if not _has_any(env, "DOUBAO_API_KEY", "ARK_API_KEY"):
            missing.append("DOUBAO_API_KEY or ARK_API_KEY")
        if not _has_any(env, "DOUBAO_MODEL", "ARK_MODEL"):
            missing.append("DOUBAO_MODEL or ARK_MODEL")
        return _provider_result(provider, missing)
    if provider == "deepseek":
        missing = [] if _has_any(env, "DEEPSEEK_API_KEY") else ["DEEPSEEK_API_KEY"]
        return _provider_result(provider, missing)
    if provider in {"openai-compatible", "compatible"}:
        missing = []
        if not _has_any(env, "OPENAI_COMPATIBLE_API_KEY"):
            missing.append("OPENAI_COMPATIBLE_API_KEY")
        if not _has_any(env, "OPENAI_COMPATIBLE_BASE_URL"):
            missing.append("OPENAI_COMPATIBLE_BASE_URL")
        if not _has_any(env, "OPENAI_COMPATIBLE_MODEL"):
            missing.append("OPENAI_COMPATIBLE_MODEL")
        return _provider_result(provider, missing)
    return _mock_or_unsupported(provider, "doubao/deepseek/openai-compatible")


def _check_embedding(env: dict[str, str]) -> dict[str, Any]:
    provider = _value(env, "JIYANGJIA_EMBEDDING_PROVIDER", "mock")
    if provider in {"doubao", "ark", "volcengine"}:
        missing = []
        if not _has_any(env, "DOUBAO_EMBEDDING_API_KEY", "EMBEDDING_API_KEY", "DOUBAO_API_KEY", "ARK_API_KEY"):
            missing.append("DOUBAO_EMBEDDING_API_KEY or EMBEDDING_API_KEY or DOUBAO_API_KEY or ARK_API_KEY")
        return _provider_result(provider, missing)
    if provider in {"openai-compatible", "compatible"}:
        missing = []
        if not _has_any(env, "OPENAI_COMPATIBLE_EMBEDDING_API_KEY", "EMBEDDING_API_KEY", "OPENAI_COMPATIBLE_API_KEY"):
            missing.append("OPENAI_COMPATIBLE_EMBEDDING_API_KEY or EMBEDDING_API_KEY or OPENAI_COMPATIBLE_API_KEY")
        if not _has_any(env, "OPENAI_COMPATIBLE_EMBEDDING_BASE_URL", "EMBEDDING_BASE_URL", "OPENAI_COMPATIBLE_BASE_URL"):
            missing.append("OPENAI_COMPATIBLE_EMBEDDING_BASE_URL or EMBEDDING_BASE_URL")
        if not _has_any(env, "OPENAI_COMPATIBLE_EMBEDDING_MODEL", "EMBEDDING_MODEL"):
            missing.append("OPENAI_COMPATIBLE_EMBEDDING_MODEL or EMBEDDING_MODEL")
        return _provider_result(provider, missing)
    return _mock_or_unsupported(provider, "doubao/openai-compatible")


def _provider_result(provider: str, missing: list[str]) -> dict[str, Any]:
    return {
        "provider": provider,
        "ready": not missing,
        "missing": missing,
    }


def _mock_or_unsupported(provider: str, expected: str) -> dict[str, Any]:
    if provider == "mock":
        return {"provider": provider, "ready": True, "missing": [], "note": "mock provider is not real MVP"}
    return {"provider": provider, "ready": False, "missing": [f"UNSUPPORTED_PROVIDER expected {expected}"]}


def _has_any(env: dict[str, str], *keys: str) -> bool:
    return any(bool(env.get(key, "").strip()) for key in keys)


def _value(env: dict[str, str], key: str, default: str) -> str:
    return env.get(key, default).strip().lower() or default


if __name__ == "__main__":
    raise SystemExit(main())
