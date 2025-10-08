from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_session,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

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

class Base(DeclarativeBase):
    pass

# Dependency для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()