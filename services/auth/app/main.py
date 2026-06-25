from fastapi import FastAPI

from .presentation.http.routes import router


def create_app() -> FastAPI:
    """Создать HTTP-приложение сервиса аутентификации."""
    app = FastAPI(title="ForkFlow Auth Service", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()
