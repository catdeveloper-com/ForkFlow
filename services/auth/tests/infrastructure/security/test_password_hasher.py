from services.auth.app.domain.value_objects import PasswordHash, RawPassword
from services.auth.app.infrastructure.security.password_hasher import Argon2PasswordHasher


def test_argon2_password_hasher_returns_password_hash() -> None:
    password_hasher = Argon2PasswordHasher()

    password_hash = password_hasher.hash(RawPassword("strong-password"))

    assert isinstance(password_hash, PasswordHash)
    assert password_hash.value.startswith("$argon2")


def test_argon2_password_hasher_does_not_store_plaintext_password() -> None:
    password_hasher = Argon2PasswordHasher()
    raw_password = RawPassword("strong-password")

    password_hash = password_hasher.hash(raw_password)

    assert password_hash.value != raw_password.value


def test_argon2_password_hasher_uses_salt() -> None:
    password_hasher = Argon2PasswordHasher()
    raw_password = RawPassword("strong-password")

    first_hash = password_hasher.hash(raw_password)
    second_hash = password_hasher.hash(raw_password)

    assert first_hash != second_hash
