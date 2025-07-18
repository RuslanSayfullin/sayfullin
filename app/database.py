import os
from dotenv import load_dotenv

# Асинхронное подключение (asyncpg + SQLAlchemy)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# Формат подключения: postgresql+asyncpg://user:password@host:port/dbname
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # Берёт значение из .env

# Асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Получение сессии (для Dependency Injection в FastAPI)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session   # Сессия передаётся в эндпоинт, а после закрывается






