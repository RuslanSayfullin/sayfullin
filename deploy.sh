#!/bin/bash

set -e

echo "🚀 Starting deployment of Todo App..."

# Обновляем сервер
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
echo "🔧 Installing required packages..."
sudo apt install -y docker.io docker-compose nginx git

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Создаем директорию проекта
sudo mkdir -p /opt/todo-app
sudo chown $USER:$USER /opt/todo-app

# Копируем файлы проекта (предполагается, что файлы уже загружены)
echo "📁 Copying project files..."
cp -r . /opt/todo-app/

cd /opt/todo-app

# Даем права на выполнение скриптов
chmod +x backend/run.sh
chmod +x frontend/build.sh
chmod +x deploy.sh

# Останавливаем существующие контейнеры
echo "🛑 Stopping existing containers..."
sudo docker-compose down || true

# Запускаем приложение через Docker Compose
echo "🐳 Starting application with Docker Compose..."
sudo docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Проверяем статус сервисов
echo "🔍 Checking services status..."

# Проверяем бэкенд
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Проверяем фронтенд
if curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ Frontend is running successfully"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "🌐 Your application is available at:"
echo "   Frontend: http://$(curl -s ifconfig.me)"
echo "   Backend API: http://$(curl -s ifconfig.me):8000"
echo "   API Documentation: http://$(curl -s ifconfig.me):8000/docs"