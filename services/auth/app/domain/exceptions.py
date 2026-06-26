class DomainError(Exception):
    """Базовая ошибка доменного слоя Auth-сервиса."""


class InvalidEmailError(DomainError):
    """Ошибка некорректного email-адреса."""


class WeakPasswordError(DomainError):
    """Ошибка слабого пароля."""


class InvalidPasswordHashError(DomainError):
    """Ошибка некорректного хеша пароля."""
