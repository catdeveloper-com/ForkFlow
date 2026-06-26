from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from .value_objects import Email


@dataclass(frozen=True, slots=True)
class User:
    """Пользователь Auth-сервиса.

    Сущность описывает только доменные данные пользователя и не знает о
    PostgreSQL, SQLAlchemy, FastAPI, JWT или сессиях.

    Attributes:
        id: Уникальный идентификатор пользователя.
        email: Email-адрес пользователя.
        created_at: Дата и время создания пользователя.
    """

    id: UUID
    email: Email
    created_at: datetime

    @classmethod
    def create(
        cls,
        email: Email,
        *,
        user_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> "User":
        """Создать доменную сущность пользователя.

        Args:
            email: Email-адрес пользователя.
            user_id: Идентификатор пользователя. Если не передан, создаётся UUID.
            created_at: Время создания. Если не передано, используется текущее UTC-время.

        Returns:
            Новая сущность пользователя.
        """
        return cls(
            id=user_id or uuid4(),
            email=email,
            created_at=created_at or datetime.now(UTC),
        )
