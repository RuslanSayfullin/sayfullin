
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, close_db
from app.config import settings
from app.api import routes, users, posts, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - выполняется ПРИ ЗАПУСКЕ приложени
    await init_db()
    print("✅ Database initialized")
    
    yield   # здесь приложение работает и обрабатывает запросы

    # Shutdown - выполняется ПРИ ЗАВЕРШЕНИИ приложения
    await close_db()
    print("✅ Database connections closed")

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

# Include routers
app.include_router(routes.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(health.router)

def run_app():
    """Function to run the application"""
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        workers=settings.app_workers,
        reload=settings.app_debug
    )

if __name__ == "__main__":
    run_app()