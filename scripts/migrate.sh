#!/bin/bash
# Скрипт для работы с миграциями базы данных

set -e

COMMAND=${1:-"upgrade"}

echo "Running Alembic migrations: $COMMAND"

case $COMMAND in
    "upgrade")
        echo "Applying all migrations..."
        docker compose exec backend alembic upgrade head
        ;;
    "downgrade")
        echo "Reverting last migration..."
        docker compose exec backend alembic downgrade -1
        ;;
    "revision")
        MESSAGE=${2:-"auto migration"}
        echo "Creating new migration: $MESSAGE"
        docker compose exec backend alembic revision --autogenerate -m "$MESSAGE"
        ;;
    "history")
        echo "Showing migration history..."
        docker compose exec backend alembic history
        ;;
    "current")
        echo "Showing current migration version..."
        docker compose exec backend alembic current
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Available commands: upgrade, downgrade, revision, history, current"
        exit 1
        ;;
esac

echo "Migration operation completed!"
