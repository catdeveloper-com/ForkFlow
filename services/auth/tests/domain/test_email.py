import pytest

from services.auth.app.domain.exceptions import InvalidEmailError
from services.auth.app.domain.value_objects import Email


def test_email_normalizes_value() -> None:
    email = Email("  USER@Example.COM  ")

    assert email.value == "user@example.com"
    assert str(email) == "user@example.com"


@pytest.mark.parametrize(
    "raw_email",
    [
        "",
        "plain-text",
        "missing-domain@",
        "@missing-local-part.com",
        "two words@example.com",
    ],
)
def test_email_rejects_invalid_value(raw_email: str) -> None:
    with pytest.raises(InvalidEmailError):
        Email(raw_email)
