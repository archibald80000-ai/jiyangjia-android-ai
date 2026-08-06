from __future__ import annotations

import os
from dataclasses import dataclass


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class Settings:
    app_name: str = "jiyangjia-gateway"
    app_version: str = "0.1.0-task008"
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
                "DOUBAO_TTS_KEY": "configured" if os.environ.get("DOUBAO_TTS_KEY") else "missing",
                "ARK_API_KEY": "configured" if os.environ.get("ARK_API_KEY") else "missing",
                "OPENAI_COMPATIBLE_API_KEY": "configured" if os.environ.get("OPENAI_COMPATIBLE_API_KEY") else "missing",
                "EMBEDDING_API_KEY": "configured" if os.environ.get("EMBEDDING_API_KEY") else "missing",
            },
        }


def load_settings() -> Settings:
    return Settings(
        max_record_seconds=int(_env("JIYANGJIA_MAX_RECORD_SECONDS", "20")),
        max_upload_bytes=int(_env("JIYANGJIA_MAX_UPLOAD_BYTES", str(5 * 1024 * 1024))),
        asr_provider=_env("JIYANGJIA_ASR_PROVIDER", "mock"),
        tts_provider=_env("JIYANGJIA_TTS_PROVIDER", "mock"),
        llm_provider=_env("JIYANGJIA_LLM_PROVIDER", "mock"),
        embedding_provider=_env("JIYANGJIA_EMBEDDING_PROVIDER", "mock"),
        knowledge_db_path=_env("JIYANGJIA_KNOWLEDGE_DB_PATH", ":memory:"),
    )
