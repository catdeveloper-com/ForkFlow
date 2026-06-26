from datetime import UTC, datetime
from uuid import UUID

from services.auth.app.domain.entities import User
from services.auth.app.domain.value_objects import Email, PasswordHash


def test_user_create_returns_domain_entity() -> None:
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    created_at = datetime(2026, 6, 26, 12, 0, tzinfo=UTC)
    email = Email("user@example.com")
    password_hash = PasswordHash("hashed-password")

    user = User.create(
        email,
        password_hash,
        user_id=user_id,
        created_at=created_at,
    )

    assert user.id == user_id
    assert user.email == email
    assert user.password_hash == password_hash
    assert user.created_at == created_at
