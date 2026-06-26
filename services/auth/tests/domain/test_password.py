import pytest

from services.auth.app.domain.exceptions import InvalidPasswordHashError, WeakPasswordError
from services.auth.app.domain.value_objects import PasswordHash, RawPassword


def test_raw_password_accepts_strong_enough_value() -> None:
    password = RawPassword("strong-password")

    assert password.value == "strong-password"


@pytest.mark.parametrize(
    "raw_password",
    [
        "",
        "       ",
        "short",
    ],
)
def test_raw_password_rejects_weak_value(raw_password: str) -> None:
    with pytest.raises(WeakPasswordError):
        RawPassword(raw_password)


def test_password_hash_accepts_non_empty_value() -> None:
    password_hash = PasswordHash("hashed-password")

    assert password_hash.value == "hashed-password"


@pytest.mark.parametrize("raw_hash", ["", "   "])
def test_password_hash_rejects_empty_value(raw_hash: str) -> None:
    with pytest.raises(InvalidPasswordHashError):
        PasswordHash(raw_hash)
