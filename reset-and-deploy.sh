#!/bin/bash

# Скрипт для полной очистки и развертывания проекта Psychology Bot (PRODUCTION)
# Использование: ./reset-and-deploy.sh

set -e  # Останавливаем при ошибке

echo "=========================================="
echo "🚀 Psychology Bot - Production Deployment"
echo "=========================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}⚠️  ВНИМАНИЕ: Это удалит ВСЕ данные!${NC}"
echo "   - Docker контейнеры"
echo "   - Docker образы"
echo "   - Docker volumes (включая базу данных)"
echo "   - Docker networks"
echo ""
read -p "Продолжить? (yes/no): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]
then
    echo "❌ Отменено"
    exit 1
fi

echo ""
echo "=========================================="
echo "🛑 Шаг 1: Остановка всех контейнеров"
echo "=========================================="
docker compose down -v 2>/dev/null || true
docker compose -f docker-compose.dev.yml down -v 2>/dev/null || true
echo -e "${GREEN}✅ Контейнеры остановлены${NC}"

echo ""
echo "=========================================="
echo "🗑️  Шаг 2: Удаление Docker образов"
echo "=========================================="
docker rmi psychologist-bot-backend 2>/dev/null || echo "Образ backend не найден"
docker rmi psychologist-bot-telegram-bot 2>/dev/null || echo "Образ telegram-bot не найден"
docker rmi psychologist-bot-frontend 2>/dev/null || echo "Образ frontend не найден"
echo -e "${GREEN}✅ Образы удалены${NC}"

echo ""
echo "=========================================="
echo "🗑️  Шаг 3: Удаление Docker volumes"
echo "=========================================="
docker volume rm psychologist-bot_postgres_data 2>/dev/null || echo "Volume postgres_data не найден"
docker volume rm psychologist-bot_postgres_dev_data 2>/dev/null || echo "Volume postgres_dev_data не найден"
docker volume rm psychologist-bot_backend_cache 2>/dev/null || echo "Volume backend_cache не найден"
echo -e "${GREEN}✅ Volumes удалены${NC}"

echo ""
echo "=========================================="
echo "🗑️  Шаг 4: Удаление Docker networks"
echo "=========================================="
docker network rm psychologist-bot_app-network 2>/dev/null || echo "Network не найдена"
docker network rm psychologist-bot_app-network-dev 2>/dev/null || echo "Network dev не найдена"
echo -e "${GREEN}✅ Networks удалены${NC}"

echo ""
echo "=========================================="
echo "🧹 Шаг 5: Очистка неиспользуемых ресурсов"
echo "=========================================="
docker system prune -f
echo -e "${GREEN}✅ Система очищена${NC}"

echo ""
echo "=========================================="
echo "🔨 Шаг 6: Сборка PRODUCTION образов"
echo "=========================================="
docker compose build --no-cache
echo -e "${GREEN}✅ Production образы собраны${NC}"

echo ""
echo "=========================================="
echo "🚀 Шаг 7: Запуск контейнеров в PRODUCTION режиме"
echo "=========================================="
docker compose up -d
echo -e "${GREEN}✅ Контейнеры запущены${NC}"

echo ""
echo "=========================================="
echo "⏳ Шаг 8: Ожидание готовности сервисов"
echo "=========================================="
echo "Ожидаем PostgreSQL..."
sleep 5
echo "Ожидаем Backend..."
sleep 5
echo "Ожидаем Frontend..."
sleep 3
echo "Ожидаем Telegram Bot..."
sleep 3

echo ""
echo "=========================================="
echo "📊 Шаг 9: Проверка статуса"
echo "=========================================="
docker compose ps

echo ""
echo "=========================================="
echo "✅ PRODUCTION DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📌 Доступные сервисы:"
echo "   🌐 Backend API:       http://localhost:8000"
echo "   🌐 Frontend:          http://localhost:3000"
echo "   🌐 API Docs:          http://localhost:8000/docs"
echo "   🤖 Telegram Bot:      Запущен и готов"
echo ""
echo -e "${YELLOW}NOTE: This is PRODUCTION mode:${NC}"
echo "   - DevTools are disabled"
echo "   - Optimized builds"
echo "   - No hot reload"
echo ""
echo "📋 Полезные команды:"
echo "   docker compose logs -f           # Логи всех сервисов"
echo "   docker compose logs backend      # Логи backend"
echo "   docker compose logs frontend     # Логи frontend"
echo "   docker compose logs telegram-bot # Логи бота"
echo "   docker compose ps                # Статус контейнеров"
echo "   docker compose restart frontend  # Перезапуск frontend"
echo ""
echo -e "${GREEN}🎉 Готово к работе!${NC}"
