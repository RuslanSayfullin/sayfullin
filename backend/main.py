import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.database import tasks_db
from backend.schemas import Task, TaskCreate

load_dotenv()
next_id = 1

app = FastAPI(title="Todo API", version="1.0.0")

# CORS настройки
origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
    "http://your-server-ip",
    "*"  # Для тестирования, в продакшене укажите конкретные домены
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Todo API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/api/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(
        id=next_id,
        title=task.title,
        completed=task.completed
    )
    next_id += 1
    tasks_db.append(new_task)
    return new_task

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            updated_task = Task(
                id=task_id,
                title=task.title,
                completed=task.completed
            )
            tasks_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    initial_length = len(tasks_db)
    tasks_db = [t for t in tasks_db if t.id != task_id]
    if len(tasks_db) == initial_length:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)