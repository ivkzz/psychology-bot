#!/bin/bash
# Скрипт для запуска проекта в режиме разработки

set -e

echo "Starting Psychology Bot in development mode..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env file with your configuration!"
    exit 1
fi

# Остановка контейнеров если они запущены
echo "Stopping existing containers..."
docker compose -f docker-compose.dev.yml down

# Удаление старых volumes (опционально)
# docker volume rm psychologist-bot_postgres_dev_data

# Сборка и запуск контейнеров
echo "Building and starting containers..."
docker compose -f docker-compose.dev.yml up --build

# Для запуска в фоне используйте:
# docker compose -f docker-compose.dev.yml up --build -d
