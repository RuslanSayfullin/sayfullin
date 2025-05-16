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
$ cd sayfullin/backend

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
Как развернуть ваше FastAPI-приложение на VPS с IP 176.124.210.35:

1. Подключение к VPS:
    $ ssh root@176.124.210.35
2. Установка зависимостей:
    $ sudo apt update && apt upgrade -y
    $ sudo apt install python3 python3-pip -y git ufw
    $ pip3 install fastapi uvicorn
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
7. Настройка firewall:
    ufw allow 8000
    ufw enable
    