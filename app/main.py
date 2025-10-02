from datetime import datetime
from typing import Annotated
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import database
from app.config import settings
from app.models import HealthCheckResponse, User


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - выполняется ПРИ ЗАПУСКЕ приложени
    await database.connect()
    await database.initialize_database()
    print("✅ Database connected and initialized")
    
    yield   # здесь приложение работает и обрабатывает запросы

    # Shutdown - выполняется ПРИ ЗАВЕРШЕНИИ приложения
    await database.disconnect()
    print("✅ Database disconnected")

app = FastAPI(
    title="SCADA system",
    description="Supervisory Control and Data Acquisition for robotic production",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_bd_connection():
    """
    Dependency для получения соединения с БД.
    После выполнения зависимой функции автоматически:
        * Вызывается await connection.commit() (если не было ошибок)
        * Или await connection.rollback() (при исключении)
        * Соединение возвращается в пул
    """
    async with database.get_connection() as conn:   # получает соединение из пула
        yield conn                                  # отдает соединение зависимой функции

ConnectionDep = Annotated[asyncpg.Connection, Depends(get_bd_connection)]

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "FastAPI with Poetry, AsyncPG and PostgreSQL",
        "status": "success",
        "environment": settings.app_env
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    db_healthy = await database.health_check()
    return HealthCheckResponse(
        status="healthy" if db_healthy else "unhealthy",
        database="connected" if db_healthy else "disconnected",
        timestamp=datetime.now(),
        environment=settings.app_env
    )


@app.get("/users/", response_model=list[User], tags=["Users"])
async def read_users(
    conn: ConnectionDep,
    skip: int = 0,
    limit: int = 100
)