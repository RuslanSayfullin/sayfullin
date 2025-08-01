import os
from typing import AsyncGenerator
import asyncpg
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем URL из .env
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Генератор подключений к PostgreSQL
    Использование:
    async with get_db() as conn:
        await conn.execute(...)
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()