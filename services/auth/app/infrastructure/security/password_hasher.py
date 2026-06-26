from argon2 import PasswordHasher as Argon2LibraryPasswordHasher

from services.auth.app.domain.value_objects import PasswordHash, RawPassword


class Argon2PasswordHasher:
    """Argon2-адаптер хеширования паролей."""

    def __init__(self, hasher: Argon2LibraryPasswordHasher | None = None) -> None:
        self._hasher = hasher or Argon2LibraryPasswordHasher()

    def hash(self, password: RawPassword) -> PasswordHash:
        """Создать Argon2-хеш пароля."""
        return PasswordHash(self._hasher.hash(password.value))
