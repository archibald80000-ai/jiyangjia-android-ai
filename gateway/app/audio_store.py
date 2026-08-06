from __future__ import annotations

import time
import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class AudioBlob:
    audio_id: str
    content: bytes
    content_type: str
    created_at: float


class InMemoryAudioStore:
    def __init__(self) -> None:
        self._items: dict[str, AudioBlob] = {}

    def put(self, content: bytes, content_type: str) -> AudioBlob:
        audio_id = f"aud_{uuid.uuid4().hex}"
        blob = AudioBlob(
            audio_id=audio_id,
            content=content,
            content_type=content_type,
            created_at=time.time(),
        )
        self._items[audio_id] = blob
        return blob

    def get(self, audio_id: str) -> AudioBlob | None:
        return self._items.get(audio_id)
