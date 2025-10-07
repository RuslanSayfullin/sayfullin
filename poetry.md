Создание проекта с pyproject.toml

Шаг 1. Создайте новую директорию для проекта:
bash

mkdir fastapi-sqlalchemy-app
cd fastapi-sqlalchemy-app

Шаг 2. Инициализируйте проект Poetry:
bash

poetry new fastapi-sqlalchemy-app

Шаг 3. Настройте базовый файл pyproject.toml:

    Создайте файл pyproject.toml через интерактивный режим:

bash

poetry init

    При инициализации укажите:

    Имя проекта: fastapi-sqlalchemy-app

    Версию: 0.1.0

    Описание: FastAPI application with SQLAlchemy, asyncpg and PostgreSQL

    Ваши данные как автора

    README файл: README.md

Шаг 4. Добавьте зависимости:

    Основные зависимости:

bash

poetry add fastapi==0.104.1
poetry add uvicorn[standard]==0.24.0
poetry add sqlalchemy==2.0.23
poetry add asyncpg==0.29.0
poetry add python-dotenv==1.0.0
poetry add pydantic==2.5.0
poetry add pydantic-settings==2.1.0
poetry add alembic==1.12.1
poetry add psycopg2-binary==2.9.9

    Зависимости разработки:

bash

poetry add --group dev pytest==7.4.0
poetry add --group dev pytest-asyncio==0.21.0
poetry add --group dev pytest-cov==4.1.0
poetry add --group dev httpx==0.25.0
poetry add --group dev black==23.0.0
poetry add --group dev isort==5.12.0
poetry add --group dev flake8==6.0.0

Шаг 5. Настройте дополнительные секции в pyproject.toml:

    Добавьте секцию скриптов:

toml

[tool.poetry.scripts]
start = "app.main:run_app"

    Настройте форматирование:

toml

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
filterwarnings = [
    "ignore::DeprecationWarning",
]

Шаг 6. Создайте виртуальное окружение и установите зависимости:
bash

poetry install

Важные замечания:

    Убедитесь, что у вас установлена нужная версия Python (3.11)

    После создания окружения проверьте его активацию:

bash

poetry shell

    Для проверки корректности конфигурации используйте:

bash

poetry check

Теперь у вас должен быть полностью сконфигурированный проект с нужным pyproject.toml файлом и установленным окружением.