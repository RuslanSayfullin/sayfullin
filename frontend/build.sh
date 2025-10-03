#!/bin/bash

echo "Building React frontend..."
cd /opt/todo-app/frontend

# Устанавливаем зависимости и билдим
npm install
npm run build

# Копируем билд в nginx директорию
sudo cp -r dist/* /var/www/html/

echo "Frontend build completed!"