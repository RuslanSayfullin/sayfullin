from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_session,
    AsyncSession
)

from app.config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Создаем фабрику сессий
AsyncSessionLocal = async_session(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()