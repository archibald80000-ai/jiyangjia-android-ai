from __future__ import annotations

import time

from fastapi import FastAPI
from fastapi.testclient import TestClient

from gateway.app.config import Settings
from gateway.app.public_access import (
    COOKIE_NAME,
    create_public_access_router,
    create_session_token,
    hash_public_access_password,
    verify_public_access_password,
)


TEST_PASSWORD = "test-only-public-password"


def build_client(*, configured: bool = True) -> TestClient:
    settings = Settings(
        app_env="production",
        public_gate_password_hash=hash_public_access_password(TEST_PASSWORD, salt=b"0123456789abcdef") if configured else "",
        public_gate_session_secret="test-session-secret-with-sufficient-entropy" if configured else "",
        public_gate_session_ttl_seconds=86_400,
    )
    app = FastAPI()
    app.include_router(create_public_access_router(settings))
    return TestClient(app, base_url="https://testserver")


def test_password_hash_round_trip_and_rejects_wrong_password() -> None:
    encoded = hash_public_access_password(TEST_PASSWORD, salt=b"0123456789abcdef")
    assert encoded.startswith("pbkdf2_sha256$600000$")
    assert verify_public_access_password(TEST_PASSWORD, encoded) is True
    assert verify_public_access_password("wrong-password", encoded) is False


def test_login_sets_secure_24_hour_cookie_and_unlocks_both_destinations() -> None:
    client = build_client()
    response = client.post("/api/v1/public-access/login", json={"password": TEST_PASSWORD})
    assert response.status_code == 200
    assert response.json()["expires_in"] == 86_400
    cookie = response.headers["set-cookie"]
    assert f"{COOKIE_NAME}=" in cookie
    assert "HttpOnly" in cookie
    assert "Secure" in cookie
    assert "SameSite=strict" in cookie
    assert "Max-Age=86400" in cookie

    session = client.get("/api/v1/public-access/session")
    assert session.status_code == 200
    assert session.json()["authenticated"] is True

    knowledge = client.get("/access/go/knowledge-center", follow_redirects=False)
    materials = client.get("/access/go/public-materials", follow_redirects=False)
    assert knowledge.status_code == 302
    assert knowledge.headers["location"] == "https://jiyangjia-ai.netlify.app/"
    assert materials.status_code == 302
    assert materials.headers["location"].endswith("/knowledge-public/v2.3")


def test_gate_rejects_missing_tampered_and_expired_sessions() -> None:
    client = build_client()
    missing = client.get("/access/go/knowledge-center", follow_redirects=False)
    assert missing.status_code == 401
    assert missing.json()["detail"]["code"] == "PUBLIC_ACCESS_REQUIRED"

    tampered = client.get(
        "/access/go/knowledge-center",
        headers={"Cookie": f"{COOKIE_NAME}=tampered"},
        follow_redirects=False,
    )
    assert tampered.status_code == 401

    expired = create_session_token("test-session-secret-with-sufficient-entropy", int(time.time()) - 1, nonce="expired")
    expired_response = client.get(
        "/access/go/knowledge-center",
        headers={"Cookie": f"{COOKIE_NAME}={expired}"},
        follow_redirects=False,
    )
    assert expired_response.status_code == 401


def test_invalid_password_rate_limits_fifth_failure() -> None:
    client = build_client()
    for _ in range(4):
        response = client.post("/api/v1/public-access/login", json={"password": "wrong-password"})
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "ACCESS_PASSWORD_INVALID"
    limited = client.post("/api/v1/public-access/login", json={"password": "wrong-password"})
    assert limited.status_code == 429
    assert limited.json()["detail"]["code"] == "ACCESS_RATE_LIMITED"
    assert limited.headers["retry-after"] == "900"


def test_missing_configuration_fails_closed() -> None:
    client = build_client(configured=False)
    response = client.post("/api/v1/public-access/login", json={"password": TEST_PASSWORD})
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "ACCESS_GATE_NOT_CONFIGURED"


def test_logout_clears_session_and_unknown_destination_is_not_redirected() -> None:
    client = build_client()
    assert client.post("/api/v1/public-access/login", json={"password": TEST_PASSWORD}).status_code == 200
    logout = client.post("/api/v1/public-access/logout")
    assert logout.status_code == 200
    assert logout.json()["authenticated"] is False
    assert client.get("/api/v1/public-access/session").json()["authenticated"] is False
    unknown = client.get("/access/go/not-allowed", follow_redirects=False)
    assert unknown.status_code == 404
