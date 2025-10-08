from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # Application
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_workers: int = 4
    app_debug: bool = False
    app_env: str = "production"

    # Database Pool
    db_pool_min_size: int = 5
    db_pool_max_size: int = 20
    db_pool_timeout: int = 30

    class Config:
        env_file = ".env"
        case_sensetive = False


settings = Settings()