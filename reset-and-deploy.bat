@echo off
REM Скрипт для полной очистки и развертывания проекта Psychology Bot (Windows)
REM Использование: reset-and-deploy.bat

echo ==========================================
echo ^🚀 Psychology Bot - Полное переразвертывание
echo ==========================================
echo.

echo ^⚠️  ВНИМАНИЕ: Это удалит ВСЕ данные!
echo    - Docker контейнеры
echo    - Docker образы
echo    - Docker volumes (включая базу данных)
echo    - Docker networks
echo.
set /p REPLY="Продолжить? (yes/no): "

if /i not "%REPLY%"=="yes" (
    echo ^❌ Отменено
    exit /b 1
)

echo.
echo ==========================================
echo ^🛑 Шаг 1: Остановка всех контейнеров
echo ==========================================
docker compose -f docker-compose.dev.yml down -v 2>nul
echo ^✅ Контейнеры остановлены

echo.
echo ==========================================
echo ^🗑️  Шаг 2: Удаление Docker образов
echo ==========================================
docker rmi psychologist-bot-backend 2>nul || echo Образ backend не найден
docker rmi psychologist-bot-telegram-bot 2>nul || echo Образ telegram-bot не найден
docker rmi psychologist-bot-frontend 2>nul || echo Образ frontend не найден
echo ^✅ Образы удалены

echo.
echo ==========================================
echo ^🗑️  Шаг 3: Удаление Docker volumes
echo ==========================================
docker volume rm psychologist-bot_postgres_data 2>nul || echo Volume postgres_data не найден
docker volume rm psychologist-bot_backend_cache 2>nul || echo Volume backend_cache не найден
docker volume rm psychologist-bot_telegram_cache 2>nul || echo Volume telegram_cache не найден
echo ^✅ Volumes удалены

echo.
echo ==========================================
echo ^🗑️  Шаг 4: Удаление Docker networks
echo ==========================================
docker network rm psychologist-bot_app-network-dev 2>nul || echo Network не найдена
echo ^✅ Networks удалены

echo.
echo ==========================================
echo ^🧹 Шаг 5: Очистка неиспользуемых ресурсов
echo ==========================================
docker system prune -f
echo ^✅ Система очищена

echo.
echo ==========================================
echo ^🔨 Шаг 6: Сборка образов
echo ==========================================
docker compose -f docker-compose.dev.yml build --no-cache
echo ^✅ Образы собраны

echo.
echo ==========================================
echo ^🚀 Шаг 7: Запуск контейнеров
echo ==========================================
docker compose -f docker-compose.dev.yml up -d
echo ^✅ Контейнеры запущены

echo.
echo ==========================================
echo ^⏳ Шаг 8: Ожидание готовности сервисов
echo ==========================================
echo Ожидаем PostgreSQL...
timeout /t 5 /nobreak >nul
echo Ожидаем Backend...
timeout /t 5 /nobreak >nul
echo Ожидаем Telegram Bot...
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo ^📊 Шаг 9: Проверка статуса
echo ==========================================
docker compose -f docker-compose.dev.yml ps

echo.
echo ==========================================
echo ^✅ РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!
echo ==========================================
echo.
echo ^📌 Доступные сервисы:
echo    ^🌐 Backend API:       http://localhost:8000
echo    ^🌐 Frontend:          http://localhost:3000
echo    ^🌐 PgAdmin:           http://localhost:5050
echo    ^🤖 Telegram Bot:      Запущен и готов
echo.
echo ^📋 Полезные команды:
echo    docker compose -f docker-compose.dev.yml logs -f        # Логи всех сервисов
echo    docker compose -f docker-compose.dev.yml logs backend   # Логи backend
echo    docker compose -f docker-compose.dev.yml logs telegram-bot  # Логи бота
echo    docker compose -f docker-compose.dev.yml ps             # Статус контейнеров
echo.
echo ^🎉 Готово к работе!
pause
