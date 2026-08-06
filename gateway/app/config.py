from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass


def load_local_env_file(path: str = ".env.local", *, override: bool = False) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key and (override or key not in os.environ):
            os.environ[key] = value.strip().strip('"').strip("'")


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class Settings:
    app_name: str = "jiyangjia-gateway"
    app_version: str = "0.1.0-task009"
    display_mode: str = "idle_video_voice"
    max_record_seconds: int = 20
    max_upload_bytes: int = 5 * 1024 * 1024
    subtitle_max_chars: int = 80
    accepted_audio_types: tuple[str, ...] = ("audio/wav", "audio/mpeg", "audio/mp4", "audio/aac", "audio/webm")
    asr_provider: str = "mock"
    tts_provider: str = "mock"
    llm_provider: str = "mock"
    embedding_provider: str = "mock"
    knowledge_provider: str = "sqlite_lightweight"
    knowledge_db_path: str = ":memory:"
    doubao_tts_endpoint: str = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
    doubao_tts_cluster: str = "volcano_tts"
    doubao_tts_voice_type: str = ""
    doubao_tts_speaker: str = ""
    doubao_tts_resource_id: str = "seed-tts-2.0"
    doubao_tts_encoding: str = "mp3"
    doubao_tts_sample_rate: int = 24000
    doubao_tts_speech_rate: int = -5
    doubao_tts_uid: str = "jiyangjia-gateway"
    doubao_tts_timeout_seconds: float = 25.0

    def safe_summary(self) -> dict[str, object]:
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "display_mode": self.display_mode,
            "max_record_seconds": self.max_record_seconds,
            "max_upload_bytes": self.max_upload_bytes,
            "providers": {
                "asr": self.asr_provider,
                "tts": self.tts_provider,
                "llm": self.llm_provider,
                "embedding": self.embedding_provider,
                "knowledge": self.knowledge_provider,
            },
            "secrets": {
                "DOUBAO_ASR_KEY": "configured" if os.environ.get("DOUBAO_ASR_KEY") else "missing",
                "DOUBAO_TTS_APP_ID": "configured" if os.environ.get("DOUBAO_TTS_APP_ID") else "missing",
                "DOUBAO_TTS_ACCESS_TOKEN": "configured" if _doubao_tts_token() else "missing",
                "DOUBAO_TTS_API_KEY": "configured" if os.environ.get("DOUBAO_TTS_API_KEY") else "missing",
                "DOUBAO_TTS_SPEAKER": "configured" if _doubao_tts_speaker() else "missing",
                "DOUBAO_TTS_RESOURCE_ID": "configured" if os.environ.get("DOUBAO_TTS_RESOURCE_ID") else "missing",
                "ARK_API_KEY": "configured" if os.environ.get("ARK_API_KEY") else "missing",
                "OPENAI_COMPATIBLE_API_KEY": "configured" if os.environ.get("OPENAI_COMPATIBLE_API_KEY") else "missing",
                "EMBEDDING_API_KEY": "configured" if os.environ.get("EMBEDDING_API_KEY") else "missing",
            },
        }


def _doubao_tts_token() -> str | None:
    return os.environ.get("DOUBAO_TTS_ACCESS_TOKEN") or os.environ.get("DOUBAO_TTS_TOKEN") or os.environ.get("DOUBAO_TTS_KEY")


def _doubao_tts_speaker() -> str | None:
    return os.environ.get("DOUBAO_TTS_SPEAKER") or os.environ.get("DOUBAO_TTS_VOICE_TYPE")


def load_settings(env_file: str = ".env.local", *, override_env_file: bool = False) -> Settings:
    load_local_env_file(env_file, override=override_env_file)
    return Settings(
        max_record_seconds=int(_env("JIYANGJIA_MAX_RECORD_SECONDS", "20")),
        max_upload_bytes=int(_env("JIYANGJIA_MAX_UPLOAD_BYTES", str(5 * 1024 * 1024))),
        asr_provider=_env("JIYANGJIA_ASR_PROVIDER", "mock"),
        tts_provider=_env("JIYANGJIA_TTS_PROVIDER", "mock"),
        llm_provider=_env("JIYANGJIA_LLM_PROVIDER", "mock"),
        embedding_provider=_env("JIYANGJIA_EMBEDDING_PROVIDER", "mock"),
        knowledge_db_path=_env("JIYANGJIA_KNOWLEDGE_DB_PATH", ":memory:"),
        doubao_tts_endpoint=_env("DOUBAO_TTS_ENDPOINT", "https://openspeech.bytedance.com/api/v3/tts/unidirectional"),
        doubao_tts_cluster=_env("DOUBAO_TTS_CLUSTER", "volcano_tts"),
        doubao_tts_voice_type=_env("DOUBAO_TTS_VOICE_TYPE", ""),
        doubao_tts_speaker=_env("DOUBAO_TTS_SPEAKER", ""),
        doubao_tts_resource_id=_env("DOUBAO_TTS_RESOURCE_ID", "seed-tts-2.0"),
        doubao_tts_encoding=_env("DOUBAO_TTS_ENCODING", "mp3"),
        doubao_tts_sample_rate=int(_env("DOUBAO_TTS_SAMPLE_RATE", "24000")),
        doubao_tts_speech_rate=int(_env("DOUBAO_TTS_SPEECH_RATE", "-5")),
        doubao_tts_uid=_env("DOUBAO_TTS_UID", "jiyangjia-gateway"),
        doubao_tts_timeout_seconds=float(_env("DOUBAO_TTS_TIMEOUT_SECONDS", "25")),
    )
