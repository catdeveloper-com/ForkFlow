class ApplicationError(Exception):
    """Базовая ошибка слоя сценариев Auth-сервиса."""


class EmailAlreadyRegisteredError(ApplicationError):
    """Ошибка регистрации пользователя с уже занятым email-адресом."""
