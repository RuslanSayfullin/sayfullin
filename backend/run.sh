#!/bin/bash

echo "Starting FastAPI backend..."
cd /opt/todo-app/backend

# Активируем виртуальное окружение если есть
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем приложение
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000