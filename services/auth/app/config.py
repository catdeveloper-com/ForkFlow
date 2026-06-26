from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """Настройки Auth-сервиса.

    Attributes:
        service_title: Название сервиса для метаданных FastAPI.
        service_version: Версия сервиса для метаданных FastAPI.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AUTH_",
        extra="ignore",
    )

    service_title: str = "ForkFlow Auth Service"
    service_version: str = "0.1.0"


def load_settings() -> AuthSettings:
    """Загрузить настройки Auth-сервиса из окружения и `.env`."""
    return AuthSettings()
