from __future__ import annotations

import asyncio
import gzip
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

import websockets

from .config import Settings
from .tts import ProviderCallError, ProviderConfigurationError


FULL_CLIENT_REQUEST = 0x1
AUDIO_ONLY_REQUEST = 0x2
FULL_SERVER_RESPONSE = 0x9
SERVER_ACK = 0xB
SERVER_ERROR_RESPONSE = 0xF

NO_SEQUENCE = 0x0
POS_SEQUENCE = 0x1
NEG_WITH_SEQUENCE = 0x3

NO_SERIALIZATION = 0x0
JSON_SERIALIZATION = 0x1
GZIP = 0x1


@dataclass(frozen=True)
class DoubaoASRConfig:
    app_id: str | None
    access_token: str | None
    api_key: str | None
    endpoint: str
    resource_id: str
    audio_format: str
    uid: str
    chunk_bytes: int
    timeout_seconds: float
    boosting_table_id: str = ""
    boosting_table_name: str = ""
    context_json: str = ""

    @classmethod
    def from_settings(cls, settings: Settings) -> "DoubaoASRConfig":
        app_id = os.environ.get("DOUBAO_ASR_APP_ID") or os.environ.get("DOUBAO_REALTIME_APP_ID")
        access_token = (
            os.environ.get("DOUBAO_ASR_ACCESS_TOKEN")
            or os.environ.get("DOUBAO_ASR_TOKEN")
            or os.environ.get("DOUBAO_ASR_KEY")
            or os.environ.get("DOUBAO_REALTIME_ACCESS_TOKEN")
        )
        api_key = os.environ.get("DOUBAO_ASR_API_KEY")
        values = {
            "DOUBAO_ASR_AUTH": api_key or (app_id and access_token),
            "DOUBAO_ASR_RESOURCE_ID": settings.doubao_asr_resource_id,
        }
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise ProviderConfigurationError(missing)
        return cls(
            app_id=app_id,
            access_token=access_token,
            api_key=api_key,
            endpoint=settings.doubao_asr_endpoint,
            resource_id=settings.doubao_asr_resource_id,
            audio_format=settings.doubao_asr_audio_format,
            uid=settings.doubao_asr_uid,
            chunk_bytes=max(3200, settings.doubao_asr_chunk_bytes),
            timeout_seconds=settings.doubao_asr_timeout_seconds,
            boosting_table_id=settings.doubao_asr_boosting_table_id,
            boosting_table_name=settings.doubao_asr_boosting_table_name,
            context_json=settings.doubao_asr_context_json,
        )


class DoubaoASRProvider:
    name = "doubao"

    def __init__(
        self,
        config: DoubaoASRConfig,
        connect: Callable[..., Awaitable[Any]] | None = None,
    ) -> None:
        self.config = config
        self._connect = connect

    async def transcribe(self, audio: bytes, content_type: str, request_id: str) -> dict[str, object]:
        if not audio:
            raise ProviderCallError("EMPTY_AUDIO", "audio must not be empty", retryable=False)
        normalized_audio, normalized_content_type = await asyncio.to_thread(_normalize_audio_for_asr, audio, content_type)
        audio_format = _audio_format(normalized_content_type, self.config.audio_format)
        payload = {
            "user": {"uid": self.config.uid},
            "audio": {
                "format": audio_format,
                "codec": "raw",
                "rate": 16000,
                "bits": 16,
                "channel": 1,
            },
            "request": build_asr_request(self.config),
        }
        headers = self._headers(request_id)
        try:
            transcript = await asyncio.wait_for(
                self._run_websocket(payload, normalized_audio, headers),
                timeout=self.config.timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            raise ProviderCallError("ASR_TIMEOUT", "Doubao ASR request timed out", retryable=True) from exc
        text = _extract_text(transcript)
        if not text:
            raise ProviderCallError("ASR_NO_TEXT", "Doubao ASR response did not include text", retryable=True)
        return {
            "text": text,
            "provider": self.name,
            "language": "zh-CN",
            "confidence": None,
            "content_type": content_type,
            "normalized_content_type": normalized_content_type,
            "raw_status": transcript.get("code") or transcript.get("status") or "ok",
        }

    def _headers(self, request_id: str) -> dict[str, str]:
        headers = {
            "X-Api-Resource-Id": self.config.resource_id,
            "X-Api-Connect-Id": request_id or str(uuid.uuid4()),
        }
        if self.config.api_key:
            headers["X-Api-Key"] = self.config.api_key
        elif self.config.app_id and self.config.access_token:
            headers["X-Api-App-Key"] = self.config.app_id
            headers["X-Api-Access-Key"] = self.config.access_token
        else:
            raise ProviderConfigurationError(["DOUBAO_ASR_AUTH"])
        return headers
    async def _run_websocket(self, payload: dict[str, Any], audio: bytes, headers: dict[str, str]) -> dict[str, Any]:
        connect = self._connect or _websocket_connect
        connection = await connect(self.config.endpoint, headers=headers, max_size=100_000_000)
        async with connection as websocket:
            await websocket.send(build_client_packet(FULL_CLIENT_REQUEST, POS_SEQUENCE, JSON_SERIALIZATION, 1, payload))
            latest: dict[str, Any] = {}
            for sequence, offset in enumerate(range(0, len(audio), self.config.chunk_bytes), start=2):
                chunk = audio[offset : offset + self.config.chunk_bytes]
                is_last = offset + self.config.chunk_bytes >= len(audio)
                flags = NEG_WITH_SEQUENCE if is_last else POS_SEQUENCE
                seq = -sequence if is_last else sequence
                await websocket.send(build_client_packet(AUDIO_ONLY_REQUEST, flags, NO_SERIALIZATION, seq, chunk))
                if not is_last:
                    latest = await _drain_available_response(websocket, latest)
                    if latest.get("_is_last_package") and _extract_text(latest):
                        return latest
                elif _extract_text(latest):
                    return latest
            while True:
                frame = await websocket.recv()
                parsed = parse_server_packet(frame)
                if parsed.get("payload"):
                    latest = parsed["payload"]
                if parsed.get("is_last_package") or _extract_text(latest):
                    return latest


def build_asr_request(config: DoubaoASRConfig) -> dict[str, object]:
    request: dict[str, object] = {
        "model_name": "bigmodel",
        "enable_itn": True,
        "enable_punc": True,
        "enable_ddc": True,
    }
    if config.boosting_table_id:
        request["corpus"] = {"boosting_table_id": config.boosting_table_id}
    elif config.boosting_table_name:
        request["corpus"] = {"boosting_table_name": config.boosting_table_name}
    if config.context_json:
        try:
            context = json.loads(config.context_json)
        except json.JSONDecodeError as exc:
            raise ProviderConfigurationError(["DOUBAO_ASR_CONTEXT_JSON"]) from exc
        if not isinstance(context, dict):
            raise ProviderConfigurationError(["DOUBAO_ASR_CONTEXT_JSON"])
        request["context"] = json.dumps(context, ensure_ascii=False, separators=(",", ":"))
    return request


async def _websocket_connect(endpoint: str, headers: dict[str, str], max_size: int):
    try:
        return await websockets.connect(endpoint, additional_headers=headers, max_size=max_size)
    except TypeError:
        return await websockets.connect(endpoint, extra_headers=headers, max_size=max_size)


async def _drain_available_response(websocket: Any, latest: dict[str, Any]) -> dict[str, Any]:
    try:
        frame = await asyncio.wait_for(websocket.recv(), timeout=0.001)
    except asyncio.TimeoutError:
        return latest
    parsed = parse_server_packet(frame)
    payload = parsed.get("payload")
    if isinstance(payload, dict):
        if parsed.get("is_last_package"):
            payload["_is_last_package"] = True
        return payload
    return latest


def build_client_packet(message_type: int, flags: int, serialization: int, sequence: int, payload: dict[str, Any] | bytes) -> bytes:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8") if isinstance(payload, dict) else payload
    compressed = gzip.compress(body)
    header = bytes(
        [
            (0x1 << 4) | 0x1,
            (message_type << 4) | flags,
            (serialization << 4) | GZIP,
            0x00,
        ]
    )
    return header + int(sequence).to_bytes(4, "big", signed=True) + len(compressed).to_bytes(4, "big", signed=False) + compressed


def parse_server_packet(packet: bytes) -> dict[str, Any]:
    if len(packet) < 8:
        raise ProviderCallError("ASR_BAD_RESPONSE", "Doubao ASR returned a short frame", retryable=True)
    header_size = (packet[0] & 0x0F) * 4
    message_type = packet[1] >> 4
    flags = packet[1] & 0x0F
    serialization = packet[2] >> 4
    compression = packet[2] & 0x0F
    cursor = header_size
    result: dict[str, Any] = {"message_type": message_type, "is_last_package": bool(flags & 0x02)}
    if flags in {POS_SEQUENCE, NEG_WITH_SEQUENCE} and len(packet) >= cursor + 4:
        result["seq"] = int.from_bytes(packet[cursor : cursor + 4], "big", signed=True)
        cursor += 4
    if message_type == SERVER_ERROR_RESPONSE:
        if len(packet) < cursor + 8:
            raise ProviderCallError("ASR_BAD_RESPONSE", "Doubao ASR returned a bad error frame", retryable=True)
        code = int.from_bytes(packet[cursor : cursor + 4], "big", signed=False)
        size = int.from_bytes(packet[cursor + 4 : cursor + 8], "big", signed=False)
        message = packet[cursor + 8 : cursor + 8 + size]
        if compression == GZIP:
            message = gzip.decompress(message)
        raise ProviderCallError("ASR_PROVIDER_ERROR", f"Doubao ASR error {code}: {message.decode('utf-8', 'replace')}", retryable=True)
    if len(packet) < cursor + 4:
        return result
    size = int.from_bytes(packet[cursor : cursor + 4], "big", signed=False)
    body = packet[cursor + 4 : cursor + 4 + size]
    if compression == GZIP and body:
        body = gzip.decompress(body)
    if serialization == JSON_SERIALIZATION and body:
        try:
            result["payload"] = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ProviderCallError("ASR_BAD_RESPONSE", "Doubao ASR returned invalid JSON", retryable=True) from exc
    return result


def _extract_text(payload: dict[str, Any]) -> str:
    candidates = [
        payload.get("text"),
        payload.get("result", {}).get("text") if isinstance(payload.get("result"), dict) else None,
        payload.get("payload", {}).get("result", {}).get("text") if isinstance(payload.get("payload"), dict) else None,
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    result = payload.get("result")
    if isinstance(result, list):
        text = "".join(item.get("text", "") for item in result if isinstance(item, dict))
        return text.strip()
    return ""


def _audio_format(content_type: str, default: str) -> str:
    normalized = content_type.split(";")[0].lower()
    mapping = {
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/mpeg": "mp3",
        "audio/mp3": "mp3",
        "audio/mp4": "mp4",
        "audio/aac": "aac",
        "audio/webm": "webm",
        "audio/pcm": "pcm",
    }
    return mapping.get(normalized, default)


def _normalize_audio_for_asr(audio: bytes, content_type: str) -> tuple[bytes, str]:
    normalized = content_type.split(";")[0].lower()
    if normalized in {"audio/wav", "audio/x-wav", "audio/pcm"}:
        return audio, normalized
    with tempfile.TemporaryDirectory(prefix="jiyangjia-asr-") as tmp:
        input_path = Path(tmp) / "input.audio"
        output_path = Path(tmp) / "output.wav"
        input_path.write_bytes(audio)
        command = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(input_path),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ProviderCallError("ASR_AUDIO_CONVERSION_FAILED", "audio normalization failed before ASR", retryable=False) from exc
        if completed.returncode != 0 or not output_path.exists():
            raise ProviderCallError("ASR_AUDIO_CONVERSION_FAILED", "audio normalization failed before ASR", retryable=False)
        return output_path.read_bytes(), "audio/wav"
