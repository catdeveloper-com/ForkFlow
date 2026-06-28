from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.auth.app.config import AuthSettings


def create_session_factory(settings: AuthSettings) -> async_sessionmaker[AsyncSession]:
    """Создать фабрику async SQLAlchemy-сессий."""
    engine = create_async_engine(settings.database_url)
    return async_sessionmaker(engine, expire_on_commit=False)


async def gen_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Отдать async SQLAlchemy-сессию и закрыть её после использования."""
    async with session_factory() as session:
        yield session
