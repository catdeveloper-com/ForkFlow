from dataclasses import dataclass

from services.auth.app.application.dto import RegisterUserCommand, RegisterUserResult
from services.auth.app.application.exceptions import EmailAlreadyRegisteredError
from services.auth.app.application.ports import UserRepository
from services.auth.app.domain.entities import User
from services.auth.app.domain.value_objects import Email


@dataclass(frozen=True, slots=True)
class RegisterUserUseCase:
    """Сценарий регистрации пользователя.

    Attributes:
        user_repository: Порт хранилища пользователей.
    """

    user_repository: UserRepository

    async def execute(self, command: RegisterUserCommand) -> RegisterUserResult:
        """Зарегистрировать пользователя по email.

        Args:
            command: Входные данные сценария регистрации.

        Returns:
            Результат регистрации с идентификатором и нормализованным email.

        Raises:
            InvalidEmailError: Если email не проходит доменную валидацию.
            EmailAlreadyRegisteredError: Если email уже зарегистрирован.
        """
        email = Email(command.email)
        if await self.user_repository.exists_by_email(email):
            raise EmailAlreadyRegisteredError("Пользователь с таким email уже зарегистрирован.")

        user = User.create(email)
        await self.user_repository.add(user)

        return RegisterUserResult(user_id=user.id, email=str(user.email))
