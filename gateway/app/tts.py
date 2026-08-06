from __future__ import annotations

import base64
import uuid
from dataclasses import dataclass
from typing import Any

import httpx

from .config import Settings


class ProviderConfigurationError(RuntimeError):
    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(f"BLOCKED_PROVIDER_CREDENTIALS: {', '.join(missing)}")


class ProviderCallError(RuntimeError):
    def __init__(self, code: str, message: str, retryable: bool = True) -> None:
        self.code = code
        self.retryable = retryable
        super().__init__(message)


@dataclass(frozen=True)
class DoubaoTTSConfig:
    app_id: str
    access_token: str
    cluster: str
    voice_type: str
    endpoint: str
    encoding: str
    uid: str
    timeout_seconds: float

    @classmethod
    def from_settings(cls, settings: Settings) -> "DoubaoTTSConfig":
        import os

        token = os.environ.get("DOUBAO_TTS_ACCESS_TOKEN") or os.environ.get("DOUBAO_TTS_TOKEN") or os.environ.get("DOUBAO_TTS_KEY")
        values = {
            "DOUBAO_TTS_APP_ID": os.environ.get("DOUBAO_TTS_APP_ID"),
            "DOUBAO_TTS_ACCESS_TOKEN": token,
            "DOUBAO_TTS_VOICE_TYPE": settings.doubao_tts_voice_type,
        }
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise ProviderConfigurationError(missing)
        return cls(
            app_id=str(values["DOUBAO_TTS_APP_ID"]),
            access_token=str(values["DOUBAO_TTS_ACCESS_TOKEN"]),
            cluster=settings.doubao_tts_cluster,
            voice_type=settings.doubao_tts_voice_type,
            endpoint=settings.doubao_tts_endpoint,
            encoding=settings.doubao_tts_encoding,
            uid=settings.doubao_tts_uid,
            timeout_seconds=settings.doubao_tts_timeout_seconds,
        )


class DoubaoTTSProvider:
    name = "doubao"

    def __init__(self, config: DoubaoTTSConfig, client: httpx.AsyncClient | None = None) -> None:
        self.config = config
        self._client = client

    async def synthesize(self, text: str, voice_id: str | None, request_id: str) -> dict[str, object]:
        clean_text = text.strip()
        if not clean_text:
            raise ProviderCallError("EMPTY_TEXT", "text must not be blank", retryable=False)
        payload = {
            "app": {
                "appid": self.config.app_id,
                "token": self.config.access_token,
                "cluster": self.config.cluster,
            },
            "user": {"uid": self.config.uid},
            "audio": {
                "voice_type": voice_id or self.config.voice_type,
                "encoding": self.config.encoding,
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0,
            },
            "request": {
                "reqid": request_id or str(uuid.uuid4()),
                "text": clean_text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
            },
        }
        headers = {
            "Authorization": f"Bearer; {self.config.access_token}",
            "Content-Type": "application/json",
        }
        response = await self._post(payload, headers)
        audio_bytes, content_type = _extract_audio(response, self.config.encoding)
        return {
            "provider": self.name,
            "content": audio_bytes,
            "content_type": content_type,
            "duration_ms": None,
            "voice_id": voice_id or self.config.voice_type,
            "encoding": self.config.encoding,
        }

    async def _post(self, payload: dict[str, Any], headers: dict[str, str]) -> httpx.Response:
        timeout = httpx.Timeout(self.config.timeout_seconds)
        if self._client is not None:
            response = await self._client.post(self.config.endpoint, json=payload, headers=headers, timeout=timeout)
        else:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(self.config.endpoint, json=payload, headers=headers)
        if response.status_code >= 500:
            raise ProviderCallError("TTS_PROVIDER_UNAVAILABLE", "Doubao TTS provider unavailable", retryable=True)
        if response.status_code >= 400:
            raise ProviderCallError("TTS_PROVIDER_REJECTED", "Doubao TTS request rejected", retryable=False)
        return response


def _extract_audio(response: httpx.Response, encoding: str) -> tuple[bytes, str]:
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("audio/"):
        return response.content, content_type.split(";")[0]
    try:
        payload = response.json()
    except ValueError as exc:
        raise ProviderCallError("TTS_BAD_RESPONSE", "Doubao TTS returned a non-audio response", retryable=True) from exc
    code = payload.get("code")
    if code not in (None, 0, "0"):
        raise ProviderCallError("TTS_PROVIDER_ERROR", str(payload.get("message") or "Doubao TTS provider error"), retryable=True)
    audio_base64 = payload.get("data") or payload.get("audio") or payload.get("audio_base64")
    if not isinstance(audio_base64, str) or not audio_base64:
        raise ProviderCallError("TTS_NO_AUDIO", "Doubao TTS response did not include audio data", retryable=True)
    try:
        return base64.b64decode(audio_base64), _content_type_for_encoding(encoding)
    except ValueError as exc:
        raise ProviderCallError("TTS_BAD_AUDIO", "Doubao TTS returned invalid base64 audio", retryable=True) from exc


def _content_type_for_encoding(encoding: str) -> str:
    normalized = encoding.lower()
    if normalized == "mp3":
        return "audio/mpeg"
    if normalized in {"wav", "pcm", "ogg"}:
        return f"audio/{normalized}"
    return "application/octet-stream"
