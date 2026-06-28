import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from services.auth.app.config import load_settings
from services.auth.app.infrastructure.db import models  # noqa: F401
from services.auth.app.infrastructure.db.base import Base

config = context.config
target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _get_database_url() -> str:
    return load_settings().database_url


def run_migrations_offline() -> None:
    """Запустить миграции без подключения к базе данных."""
    context.configure(
        url=_get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Запустить миграции через активное подключение."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запустить миграции с async SQLAlchemy engine."""
    config_section = config.get_section(config.config_ini_section, {})
    config_section["sqlalchemy.url"] = _get_database_url()
    connectable = async_engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
