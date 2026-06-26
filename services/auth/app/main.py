from fastapi import FastAPI

from .config import AuthSettings, load_settings
from .presentation.http.routes import router


def create_app(settings: AuthSettings | None = None) -> FastAPI:
    """Создать HTTP-приложение сервиса аутентификации."""
    settings = settings or load_settings()
    app = FastAPI(title=settings.service_title, version=settings.service_version)
    app.include_router(router)
    return app


app = create_app()
