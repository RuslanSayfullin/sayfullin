from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from models import Machine
from database import get_db


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, engineers"}

@app.post("/add-new-machine")
async def add_new_machine(machine: Machine):
    return {"machine": machine}

# Пример эндпоинта с проверкой подключения
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"status": "OK", "result": result.scalar()}