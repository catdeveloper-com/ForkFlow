import re
from dataclasses import dataclass

from .exceptions import InvalidEmailError, InvalidPasswordHashError, WeakPasswordError

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MIN_PASSWORD_LENGTH = 8


@dataclass(frozen=True, slots=True)
class Email:
    """Email-адрес пользователя.

    Value object нормализует адрес и защищает домен от заведомо некорректных
    email-значений.

    Attributes:
        value: Нормализованный email-адрес.
    """

    value: str

    def __post_init__(self) -> None:
        normalized_value = self.value.strip().lower()
        if not _EMAIL_PATTERN.fullmatch(normalized_value):
            raise InvalidEmailError("Некорректный email-адрес.")

        object.__setattr__(self, "value", normalized_value)

    def __str__(self) -> str:
        """Вернуть email-адрес строкой."""
        return self.value


@dataclass(frozen=True, slots=True)
class RawPassword:
    """Сырой пароль пользователя."""

    value: str

    def __post_init__(self) -> None:
        if len(self.value) < _MIN_PASSWORD_LENGTH or not self.value.strip():
            raise WeakPasswordError("Пароль должен содержать минимум 8 символов.")


@dataclass(frozen=True, slots=True)
class PasswordHash:
    """Хеш пароля пользователя."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidPasswordHashError("Хеш пароля не может быть пустым.")
