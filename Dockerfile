FROM python:3.11-slim
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копирование приложения
COPY app/ ./app/
COPY .env ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]