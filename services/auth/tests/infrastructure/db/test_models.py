from sqlalchemy import UniqueConstraint

from services.auth.app.infrastructure.db.models import UserModel


def test_user_model_declares_required_columns() -> None:
    columns = UserModel.__table__.columns

    assert {
        "id",
        "email",
        "password_hash",
        "created_at",
        "updated_at",
    } <= set(columns.keys())
    assert not columns["email"].nullable
    assert not columns["password_hash"].nullable
    assert not columns["created_at"].nullable
    assert not columns["updated_at"].nullable


def test_user_model_declares_email_unique_constraint() -> None:
    unique_constraints = {
        constraint.name
        for constraint in UserModel.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_users_email" in unique_constraints
