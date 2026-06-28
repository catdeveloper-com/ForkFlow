from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """Настройки Auth-сервиса.

    Attributes:
        service_title: Название сервиса для метаданных FastAPI.
        service_version: Версия сервиса для метаданных FastAPI.
        database_url: DSN PostgreSQL для Auth-сервиса.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AUTH_",
        extra="ignore",
    )

    service_title: str = "ForkFlow Auth Service"
    service_version: str = "0.1.0"
    database_url: str = (
        "postgresql+asyncpg://forkflow:local-development-only-change-me"
        "@localhost:5432/forkflow_auth"
    )


def load_settings() -> AuthSettings:
    """Загрузить настройки Auth-сервиса из окружения и `.env`."""
    return AuthSettings()
