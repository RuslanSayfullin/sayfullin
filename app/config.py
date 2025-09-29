from typing import Optional

# Специализированный класс для работы с настройками приложения
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # создаем конфигурацию приложения
    database_url: str   # URL базы данных

    # Параметры с значениями по умолчанию
    app_host: str = "0.0.0.0"      # Хост для запуска сервера
    app_port: int = 8000           # Порт сервера
    app_workers: int = 4           # Количество worker-процессов
    app_debug: bool = False        # Режим отладки
    app_env: str = "production"    # Окружение (production/development)

    # Настройки пула соединений с БД
    db_pool_min_size: int = 5      # Минимальное количество соединений
    db_pool_max_size: int = 20     # Максимальное количество соединений  
    db_pool_timeout: int = 30      # Таймаут соединения в секундах

    class Config:
        env_file = ".env"          # Читать настройки из .env файла
        case_sensitive = False     # Игнорировать регистр переменных

settings = Settings()  # Создает объект с загруженными настройками