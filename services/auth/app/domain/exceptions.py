class DomainError(Exception):
    """Базовая ошибка доменного слоя Auth-сервиса."""


class InvalidEmailError(DomainError):
    """Ошибка некорректного email-адреса."""
