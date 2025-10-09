##### _разработка Sayfullin R.R.
##### реализация я с FastAPI (бэкенд) и JavaScript (фронтенд) для регистрации и авторизации:

Инструкция актуальна для Linux-систем.
========================================================================================================================
Используемые технологии:
    python = "^3.11"
    fastapi= "^0.115.12"
    PostgreSQL

Скопируйте репозиторий с помощью команды:
$ git clone https://github.com/RuslanSayfullin/sayfullin.git
Перейдите в основную директорию с помощью команды: 
$ cd sayfullin/app

Интерактивная документация: http://localhost:8000/docs

========================================================================================================================
# Создать и активировать виртуальное окружение: 
    $ poetry env use python3.11
    $ poetry shell
# Установить зависимости:
    $ poetry install 
# Выход:
    $ exit
# Посмотреть список всех окружений
    $ poetry env list
# Удалить текущее активное окружение
    $ poetry env remove <имя_окружения>
# Вывести дерево зависимостей
    $ poetry shoe --tree


========================================================================================================================
Установка Postgres на VDS (Ubuntu/Debian)
Запускаем утилиту psql как пользователь postgres с правами sudo.
    $ sudo -u postgres psql
Создать БД:
    =# CREATE DATABASE portal;
Посмотреть список доступных баз данных:
    =# SELECT datname FROM pg_database;
Удалить базу данных:
    =# DROP DATABASE имя_базы;

Создание пользователя:
    =# CREATE USER portaluser WITH PASSWORD 'myPassword';
Даем права на базу командой:
    =# GRANT ALL PRIVILEGES ON DATABASE "portal" to portaluser;
Для просмотра всех пользователей:
    =# select * from pg_user;
Смена пароля:
    =# ALTER USER portaluser PASSWORD 'password'
Отозвать все привилегии от всех баз данных
    =# REVOKE ALL PRIVILEGES ON DATABASE portal FROM portaluser;
Удаление пользователя выполняется следующей командой:
    =# DROP USER portaluser;
Подключиться к базе данных:
    $ sudo -u postgres psql -d portal

Для безопасного хранения пароля и других чувствительных данных (например, в DATABASE_URL) используйте переменные окружения (environment variables).
1. Создайте файл .env в корне проекта и добаввялем переменные:

    # .env
    DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/portal
    Сгенерировать ключ командой: 
        $ openssl rand -hex 32
2. Установите python-dotenv(иблиотека загружает переменные из .env в os.environ):
    $ pip install python-dotenv

3. Загрузите переменные в код:


========================================================================================================================
