from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient

import gateway.app.main as main_module


def test_release_manifest_fails_closed_when_not_configured(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "settings", replace(main_module.settings, android_release_version_code=0))
    response = TestClient(main_module.app).get("/api/v1/client/release")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "RELEASE_NOT_CONFIGURED"


def test_release_manifest_is_etag_aware(monkeypatch) -> None:
    configured = replace(
        main_module.settings,
        android_release_version_code=42,
        android_release_version_name="1.2.3",
        android_release_apk_url="https://updates.example.invalid/jiyangjia-42.apk",
        android_release_size_bytes=123456,
        android_release_sha256="A" * 64,
        android_release_certificate_sha256="B" * 64,
        android_release_notes="controlled test release",
    )
    monkeypatch.setattr(main_module, "settings", configured)
    client = TestClient(main_module.app)
    response = client.get("/api/v1/client/release")
    assert response.status_code == 200
    assert response.json()["package"] == "ai.jiyangjia.kiosk"
    assert response.json()["version_code"] == 42
    assert response.headers["etag"]
    unchanged = client.get("/api/v1/client/release", headers={"If-None-Match": response.headers["etag"]})
    assert unchanged.status_code == 304
