from datetime import UTC, datetime
from uuid import UUID

from services.auth.app.domain.entities import User
from services.auth.app.domain.value_objects import Email


def test_user_create_returns_domain_entity() -> None:
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    created_at = datetime(2026, 6, 26, 12, 0, tzinfo=UTC)
    email = Email("user@example.com")

    user = User.create(email, user_id=user_id, created_at=created_at)

    assert user.id == user_id
    assert user.email == email
    assert user.created_at == created_at
