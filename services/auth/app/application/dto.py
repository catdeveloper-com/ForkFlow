from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    """Входные данные сценария регистрации пользователя.

    Args:
        email: Email-адрес в сыром виде, полученный от внешнего входа.
        password: Пароль в сыром виде, полученный от внешнего входа.
    """

    email: str
    password: str


@dataclass(frozen=True, slots=True)
class RegisterUserResult:
    """Результат успешной регистрации пользователя.

    Attributes:
        user_id: Уникальный идентификатор созданного пользователя.
        email: Нормализованный email-адрес пользователя.
    """

    user_id: UUID
    email: str
