#!/bin/bash

# Скрипт для перезапуска backend после изменения времени планировщика
# Использование: ./restart-scheduler.sh

echo "=========================================="
echo "🔄 Перезапуск Backend для применения нового времени"
echo "=========================================="
echo ""

# Останавливаем и удаляем контейнер backend
echo "🛑 Остановка backend..."
docker compose -f docker-compose.dev.yml stop backend
docker compose -f docker-compose.dev.yml rm -f backend

echo ""
echo "🚀 Запуск backend с новыми настройками..."
docker compose -f docker-compose.dev.yml up -d backend

echo ""
echo "⏳ Ожидание запуска backend..."
sleep 5

echo ""
echo "📋 Проверка логов backend:"
echo "=========================================="
docker compose -f docker-compose.dev.yml logs backend --tail 30 | grep -i "scheduler\|morning\|evening\|started"

echo ""
echo "=========================================="
echo "✅ Backend перезапущен!"
echo "=========================================="
echo ""
echo "📌 Проверьте настройки планировщика:"
echo "   MORNING_TASK_TIME: $(grep MORNING_TASK_TIME .env | cut -d'=' -f2)"
echo "   EVENING_REMINDER_TIME: $(grep EVENING_REMINDER_TIME .env | cut -d'=' -f2)"
echo ""
echo "💡 Планировщик автоматически отправит задания в указанное время"
echo "💡 Для ручной отправки используйте API endpoint:"
echo "   curl -X POST http://localhost:8000/api/v1/admin/scheduler/send-morning-tasks \\"
echo "     -H \"Authorization: Bearer YOUR_ADMIN_TOKEN\""
echo ""
