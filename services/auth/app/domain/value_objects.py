import re
from dataclasses import dataclass

from .exceptions import InvalidEmailError

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class Email:
    """Email-адрес пользователя.

    Value object нормализует адрес и защищает домен от заведомо некорректных
    email-значений. Он не зависит от FastAPI, Pydantic или базы данных.

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
