import asyncio

import pytest

from services.auth.app.application.dto import RegisterUserCommand
from services.auth.app.application.exceptions import EmailAlreadyRegisteredError
from services.auth.app.application.use_cases.register_user import RegisterUserUseCase
from services.auth.app.domain.entities import User
from services.auth.app.domain.exceptions import InvalidEmailError
from services.auth.app.domain.value_objects import Email


class FakeUserRepository:
    """Тестовый адаптер порта UserRepository."""

    def __init__(self, existing_emails: set[str] | None = None) -> None:
        self.existing_emails = existing_emails or set()
        self.users: list[User] = []

    async def exists_by_email(self, email: Email) -> bool:
        stored_user_emails = {str(user.email) for user in self.users}
        return str(email) in self.existing_emails | stored_user_emails

    async def add(self, user: User) -> None:
        self.users.append(user)


def test_register_user_creates_user() -> None:
    repository = FakeUserRepository()
    use_case = RegisterUserUseCase(user_repository=repository)

    result = asyncio.run(use_case.execute(RegisterUserCommand(email="  USER@Example.COM  ")))

    assert result.email == "user@example.com"
    assert len(repository.users) == 1
    assert repository.users[0].id == result.user_id
    assert str(repository.users[0].email) == "user@example.com"


def test_register_user_rejects_duplicate_email() -> None:
    repository = FakeUserRepository(existing_emails={"user@example.com"})
    use_case = RegisterUserUseCase(user_repository=repository)

    with pytest.raises(EmailAlreadyRegisteredError):
        asyncio.run(use_case.execute(RegisterUserCommand(email="USER@example.com")))

    assert repository.users == []


def test_register_user_rejects_invalid_email() -> None:
    repository = FakeUserRepository()
    use_case = RegisterUserUseCase(user_repository=repository)

    with pytest.raises(InvalidEmailError):
        asyncio.run(use_case.execute(RegisterUserCommand(email="not-email")))

    assert repository.users == []
