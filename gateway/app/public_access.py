from __future__ import annotations

import base64
import binascii
from collections import defaultdict, deque
import hashlib
import hmac
import secrets
from threading import Lock
import time
from typing import Deque

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from .config import Settings


COOKIE_NAME = "jyj_public_access"
PASSWORD_SCHEME = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 600_000
RATE_LIMIT_WINDOW_SECONDS = 15 * 60
RATE_LIMIT_FAILURES = 5
DESTINATIONS = {
    "knowledge-center": "https://jiyangjia-ai.netlify.app/",
    "public-materials": "https://github.com/archibald80000-ai/jiyangjia-android-ai/tree/main/knowledge-public/v2.3",
}


class PublicAccessLoginRequest(BaseModel):
    password: str = Field(min_length=1, max_length=256)


def _encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_public_access_password(password: str, *, salt: bytes | None = None, iterations: int = PASSWORD_ITERATIONS) -> str:
    if not password:
        raise ValueError("password must not be empty")
    if iterations < 100_000 or iterations > 2_000_000:
        raise ValueError("iterations outside supported range")
    password_salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), password_salt, iterations)
    return f"{PASSWORD_SCHEME}${iterations}${_encode(password_salt)}${_encode(digest)}"


def verify_public_access_password(password: str, encoded: str) -> bool:
    try:
        scheme, raw_iterations, encoded_salt, encoded_digest = encoded.split("$", 3)
        iterations = int(raw_iterations)
        if scheme != PASSWORD_SCHEME or iterations < 100_000 or iterations > 2_000_000:
            return False
        salt = _decode(encoded_salt)
        expected = _decode(encoded_digest)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except (TypeError, ValueError, binascii.Error):
        return False


def create_session_token(secret: str, expires_at: int, *, nonce: str | None = None) -> str:
    token_nonce = nonce or secrets.token_urlsafe(12)
    payload = f"v1.{expires_at}.{token_nonce}"
    signature = hmac.new(secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest()
    return f"{payload}.{_encode(signature)}"


def validate_session_token(token: str, secret: str, *, now: int | None = None) -> tuple[bool, int | None]:
    if not token or not secret:
        return False, None
    try:
        version, raw_expiry, nonce, encoded_signature = token.split(".", 3)
        expires_at = int(raw_expiry)
        if version != "v1" or not nonce or expires_at <= (now if now is not None else int(time.time())):
            return False, None
        payload = f"{version}.{expires_at}.{nonce}"
        expected = hmac.new(secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest()
        return hmac.compare_digest(_decode(encoded_signature), expected), expires_at
    except (TypeError, ValueError, binascii.Error):
        return False, None


class FailedLoginLimiter:
    def __init__(self) -> None:
        self._failures: dict[str, Deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def is_limited(self, client_id: str, *, now: float | None = None) -> bool:
        moment = now if now is not None else time.time()
        with self._lock:
            attempts = self._active_attempts(client_id, moment)
            return len(attempts) >= RATE_LIMIT_FAILURES

    def record_failure(self, client_id: str, *, now: float | None = None) -> bool:
        moment = now if now is not None else time.time()
        with self._lock:
            attempts = self._active_attempts(client_id, moment)
            attempts.append(moment)
            return len(attempts) >= RATE_LIMIT_FAILURES

    def clear(self, client_id: str) -> None:
        with self._lock:
            self._failures.pop(client_id, None)

    def _active_attempts(self, client_id: str, moment: float) -> Deque[float]:
        attempts = self._failures[client_id]
        cutoff = moment - RATE_LIMIT_WINDOW_SECONDS
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()
        return attempts


def _client_id(request: Request) -> str:
    peer = request.client.host if request.client else "unknown"
    if peer in {"127.0.0.1", "::1", "testclient"}:
        forwarded = request.headers.get("X-Real-IP", "").strip()
        if forwarded:
            return forwarded[:64]
    return peer[:64]


def create_public_access_router(settings: Settings) -> APIRouter:
    router = APIRouter()
    limiter = FailedLoginLimiter()
    ttl_seconds = max(300, min(settings.public_gate_session_ttl_seconds, 7 * 24 * 60 * 60))

    def configured() -> bool:
        return bool(settings.public_gate_password_hash and settings.public_gate_session_secret)

    def current_session(request: Request) -> tuple[bool, int | None]:
        token = request.cookies.get(COOKIE_NAME, "")
        return validate_session_token(token, settings.public_gate_session_secret)

    def require_session(request: Request) -> None:
        authenticated, _ = current_session(request)
        if not authenticated:
            raise HTTPException(
                status_code=401,
                detail={"code": "PUBLIC_ACCESS_REQUIRED", "message": "请先验证资料访问密码。"},
            )

    @router.post("/api/v1/public-access/login")
    def login(request: Request, body: PublicAccessLoginRequest) -> JSONResponse:
        if not configured():
            raise HTTPException(
                status_code=503,
                detail={"code": "ACCESS_GATE_NOT_CONFIGURED", "message": "资料访问门禁尚未配置。"},
            )
        client_id = _client_id(request)
        if limiter.is_limited(client_id):
            raise HTTPException(
                status_code=429,
                detail={
                    "code": "ACCESS_RATE_LIMITED",
                    "message": "尝试次数过多，请稍后再试。",
                    "retry_after_seconds": RATE_LIMIT_WINDOW_SECONDS,
                },
                headers={"Retry-After": str(RATE_LIMIT_WINDOW_SECONDS)},
            )
        if not verify_public_access_password(body.password, settings.public_gate_password_hash):
            limited = limiter.record_failure(client_id)
            if limited:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "code": "ACCESS_RATE_LIMITED",
                        "message": "尝试次数过多，请稍后再试。",
                        "retry_after_seconds": RATE_LIMIT_WINDOW_SECONDS,
                    },
                    headers={"Retry-After": str(RATE_LIMIT_WINDOW_SECONDS)},
                )
            raise HTTPException(
                status_code=401,
                detail={"code": "ACCESS_PASSWORD_INVALID", "message": "密码不正确，请重新输入。"},
            )
        limiter.clear(client_id)
        expires_at = int(time.time()) + ttl_seconds
        response = JSONResponse({"authenticated": True, "expires_in": ttl_seconds, "expires_at": expires_at})
        response.set_cookie(
            COOKIE_NAME,
            create_session_token(settings.public_gate_session_secret, expires_at),
            max_age=ttl_seconds,
            path="/",
            secure=True,
            httponly=True,
            samesite="strict",
        )
        return response

    @router.get("/api/v1/public-access/session")
    def session(request: Request) -> dict[str, object]:
        authenticated, expires_at = current_session(request)
        return {"authenticated": authenticated, "expires_at": expires_at if authenticated else None}

    @router.post("/api/v1/public-access/logout")
    def logout() -> JSONResponse:
        response = JSONResponse({"authenticated": False})
        response.delete_cookie(COOKIE_NAME, path="/", secure=True, httponly=True, samesite="strict")
        return response

    @router.get("/access/go/{destination}")
    def protected_destination(destination: str, request: Request) -> RedirectResponse:
        target = DESTINATIONS.get(destination)
        if target is None:
            raise HTTPException(status_code=404, detail={"code": "ACCESS_DESTINATION_NOT_FOUND"})
        require_session(request)
        return RedirectResponse(target, status_code=302, headers={"Cache-Control": "no-store"})

    return router
