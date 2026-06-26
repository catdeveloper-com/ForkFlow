from typing import Protocol

from services.auth.app.domain.entities import User
from services.auth.app.domain.value_objects import Email, PasswordHash, RawPassword


class UserRepository(Protocol):
    """Порт хранилища пользователей для сценариев Auth-сервиса."""

    async def exists_by_email(self, email: Email) -> bool:
        """Проверить, существует ли пользователь с таким email."""

    async def add(self, user: User) -> None:
        """Сохранить пользователя."""


class PasswordHasher(Protocol):
    """Порт хеширования пароля для сценариев Auth-сервиса."""

    def hash(self, password: RawPassword) -> PasswordHash:
        """Создать безопасный хеш пароля."""
