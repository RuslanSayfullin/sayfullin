##### _разработка Sayfullin R.R.

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

========================================================================================================================
Создать и активировать виртуальное окружение: 
    $ python3 -m venv venv 
    $ source venv/bin/activate 
Установить зависимости из файла requirements.txt:
    (venv) $ pip install -r requirements.txt

Cоздания файла зависимостейс помощью команды:
    $ pip freeze > requirements.txt

Open the inreactive documentation: http://localhost:8000/docs



========================================================================================================================
Развернуть FastAPI-приложение на VPS с IP 176.124.210.35:

1. Подключение к VPS:
    $ ssh root@176.124.210.35
2. Установка зависимостей:
    $ sudo apt update && apt upgrade -y
    $ sudo apt install python3 python3-pip -y git ufw
    $ pip3 install fastapi uvicorn pymongo python-multipart
3. Загрузка кода на сервер:
    $ git clone https://github.com/RuslanSayfullin/sayfullin.git
    $ cd sayfullin
4. Запуск приложения:
    $ uvicorn main:app --host 0.0.0.0 --port 8000
    --host 0.0.0.0  - делает приложение доступным извне
    --port 8000     - порт по умолчанию
5. Проверка работы:
    Откройте в браузере: http://176.124.210.35:8000/random
    Через curl:
        $ curl http://176.124.210.35:8000/random
6.  Использовать screen для FastAPI.
    screen — это терминальный мультиплексор, который позволяет запускать процессы в фоне, даже если SSH-сессия оборвется, процесс продолжит работу.
    Установка screen:
        $ sudo apt update && sudo apt install screen -y
    Создание сессии:
        $ screen -S fastapi  # Создаем сессию с именем "fastapi"
    Запуск сервера внутри screen:
        $ uvicorn main:app --host 0.0.0.0 --port 8000
    Отключение от сессии (без остановки процесса):
        $ Ctrl + A, затем D (Сочетание клавиш: сначала Ctrl+A, отпустить, потом нажать D)
    Возврат к сессии:
        $ screen -r fastapi  # Реатач сессии
    Просмотр всех сессий:
        $ screen -ls
7.  Чтобы остановить запущенные screen-сессии с FastAPI на VPS:
    $ screen -r 37714.fastapi  # Для Detached сессии
8. Настройка firewall:
    ufw allow 8000
    ufw enable
    




Итоговое решение:
# Копируем файл в /tmp/, даём права postgres и запускаем
$ sudo cp demo-small-20170815.sql /tmp/
$ sudo chown postgres:postgres /tmp/demo-small-20170815.sql
$ sudo -u postgres psql -f /tmp/demo-small-20170815.sql



######## Postgres
Запускаем утилиту psql как пользователь postgres с правами sudo.
    $ sudo -u postgres psql
Создать БД:
    =# CREATE DATABASE portal;
Посмотреть список доступных баз данных:
    =# SELECT datname FROM pg_database;
Удалить базу данных:
    =# DROP DATABASE имя_базы;


Создание пользователя:
    =# CREATE USER portal WITH PASSWORD 'myPassword';
Даем права на базу командой:
    =# GRANT ALL PRIVILEGES ON DATABASE "portal" to portal;
Для просмотра всех пользователей:
    =# select * from pg_user;
Смена пароля:
    =# ALTER USER portal PASSWORD 'password'
Удаление пользователя выполняется следующей командой:
    =# DROP USER portal;
Подключиться к базе данных:
    $ sudo -u postgres psql -d portal

Для безопасного хранения пароля и других чувствительных данных (например, в DATABASE_URL) используйте переменные окружения (environment variables).
1. Создайте файл .env в корне проекта и добаввялем переменные:

    # .env
    DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/postgres

2. Установите python-dotenv(иблиотека загружает переменные из .env в os.environ):
    $ pip install python-dotenv

3. Загрузите переменные в код:
