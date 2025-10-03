from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, text

from app.config import settings
from app.models import Base

# Async engine for FastAPI
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_size=settings.db_pool_min_size,
    max_overflow=settings.db_pool_max_size - settings.db_pool_min_size,
     pool_timeout=settings.db_pool_timeout,
)

# Sync engine for migrations and tests
sync_engine = create_engine(settings.sync_database_url)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully")

async def health_check():
    """Check database health"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            result.scalar()
            return True
    except Exception as e:
        print(f"❌ Database health check failed: {e}")
        return False

async def close_db():
    """Close database connections"""
    await async_engine.dispose()