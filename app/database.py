import asyncpg
from contextlib import asynccontextmanager

from app.config import settings
from typing import AsyncGenerator, Optional

class Database:
    """
    Класс для управления подключениями к базе данных PostgreSQL
    """

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Создаем пул соединений с БД"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=settings.db_pool_min_size,
                max_size=settings.db_pool_max_size,
                timeout=settings.db_pool_timeout,
                max_inactive_connection_lifetime=300    # время жизни неактивных соединений
            )
        return self.pool
    
    async def disconnect(self):
        """Закрываем пул соединений"""
        if self.pool:
            await self.pool.close()
            self.pool = None

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Контекстный менеджер для получения соединения"""
        if self.pool is None:
            await self.connect()

        async with self.pool.acquire() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    async def health_check(self) -> bool:
        """Проверка работоспособности БД"""
        try:
            async with self.get_connection() as conn:
                await conn.fetchval("SELECT 1")
                return True
        except Exception:
            return False
        
    async def initiaize_database(self):
        """Инициализация БД"""
        async with self.get_connection() as conn:
            # Создание таблицы пользователей
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )                  
            ''')

            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);                
            ''')

            # Тестовые данные
            await conn.execute('''
                INSERT INTO users (name, email) 
                VALUES 
                    ('John Doe', 'john@example.com'),
                    ('Jane Smith', 'jane@example.com')
                ON CONFLICT (email) DO NOTHING
            ''')

# Глобальный экземпляр базы данных
database = Database