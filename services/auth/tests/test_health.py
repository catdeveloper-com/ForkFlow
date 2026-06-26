from fastapi.testclient import TestClient

from services.auth.app.config import load_settings
from services.auth.app.main import create_app


def test_health_returns_auth_service_status() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "auth"}


def test_auth_settings_can_be_loaded_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_SERVICE_TITLE", "Test Auth Service")
    monkeypatch.setenv("AUTH_SERVICE_VERSION", "9.9.9")

    settings = load_settings()

    assert settings.service_title == "Test Auth Service"
    assert settings.service_version == "9.9.9"
