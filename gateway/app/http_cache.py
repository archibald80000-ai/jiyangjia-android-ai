from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import Request, Response
from fastapi.responses import JSONResponse


def payload_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest().upper()


def strong_etag(payload: dict[str, Any]) -> str:
    return f'"{payload_digest(payload)}"'


def conditional_json(
    request: Request,
    payload: dict[str, Any],
    *,
    etag: str | None = None,
    cache_control: str = "private, max-age=0, must-revalidate",
) -> Response:
    resolved_etag = etag or strong_etag(payload)
    headers = {"ETag": resolved_etag, "Cache-Control": cache_control}
    if request.headers.get("If-None-Match", "").strip() == resolved_etag:
        return Response(status_code=304, headers=headers)
    return JSONResponse(payload, headers=headers)
