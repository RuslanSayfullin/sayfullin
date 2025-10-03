import asyncio
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine

from app.models import Base
from app.database import get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
TEST_SYNC_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def test_sessionmaker(test_engine):
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

@pytest.fixture(scope="session", autouse=True)
async def create_test_tables(test_engine):
    # Create sync engine for table creation
    sync_engine = create_engine(TEST_SYNC_DATABASE_URL)
    
    # Drop and create all tables
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.dispose()
    
    yield
    
    # Cleanup
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_sessionmaker):
    async with test_sessionmaker() as session:
        yield session
        # Clean up after test
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

@pytest.fixture
def client(db_session):
    # Override dependency
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()