from contextlib import contextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import database

@contextmanager
async def lifespan(app: FastAPI):
    # Startup - выполняется ПРИ ЗАПУСКЕ приложени
    await database.connect()
    await database.initialize_database()
    print("✅ Database connected and initialized")
    
    yield   # здесь приложение работает и обрабатывает запросы

    # Shutdown - выполняется ПРИ ЗАВЕРШЕНИИ приложения
    await database.disconnect()
    print("✅ Database connections closed")

app = FastAPI(
    title="sayfullin.tech",
    description="upervisory Control and Data Acquisition for robotic production",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*",]
)