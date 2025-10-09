from contextlib import contextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db
from models import Base
from schemas import User, UserCreate
from crud import user



@contextmanager
async def lifespan(app: FastAPI):
    # Startup - выполняется ПРИ ЗАПУСКЕ приложени
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database connected and initialized")
    
    yield   # здесь приложение работает и обрабатывает запросы

    # Shutdown - выполняется ПРИ ЗАВЕРШЕНИИ приложения
    await engine.dispose()
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

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Async App"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = await user.get_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return await user.create(db=db, user_in=user)