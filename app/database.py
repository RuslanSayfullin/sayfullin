from contextlib import asynccontextmanager
from typing import Optional

import asyncpg

from app.config import settings

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Создает пул соединений с БД"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=settings.db_pool_min_size,
                max_size=settings.db_pool_max_size,
                timeout=settings.db_pool_timeout,
                max_inactive_connection_lifetime=300
            )
        return self.pool





# Глобальный экземпляр базы данных
database = Database()