@echo off
REM Скрипт для перезапуска backend после изменения времени планировщика (Windows)
REM Использование: restart-scheduler.bat

echo ==========================================
echo ^🔄 Перезапуск Backend для применения нового времени
echo ==========================================
echo.

REM Останавливаем и удаляем контейнер backend
echo ^🛑 Остановка backend...
docker compose -f docker-compose.dev.yml stop backend
docker compose -f docker-compose.dev.yml rm -f backend

echo.
echo ^🚀 Запуск backend с новыми настройками...
docker compose -f docker-compose.dev.yml up -d backend

echo.
echo ^⏳ Ожидание запуска backend...
timeout /t 5 /nobreak >nul

echo.
echo ^📋 Проверка логов backend:
echo ==========================================
docker compose -f docker-compose.dev.yml logs backend --tail 30 | findstr /i "scheduler morning evening started"

echo.
echo ==========================================
echo ^✅ Backend перезапущен!
echo ==========================================
echo.
echo ^📌 Проверьте настройки планировщика в .env файле
echo.
echo ^💡 Планировщик автоматически отправит задания в указанное время
echo ^💡 Для ручной отправки используйте API endpoint:
echo    curl -X POST http://localhost:8000/api/v1/admin/scheduler/send-morning-tasks ^
echo      -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
echo.
pause
