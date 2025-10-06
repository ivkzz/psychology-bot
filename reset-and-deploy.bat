@echo off
REM Psychology Bot - Full Reset and Deploy Script (Windows)
REM Usage: reset-and-deploy.bat

echo ==========================================
echo Psychology Bot - Full Redeploy
echo ==========================================
echo.

echo WARNING: This will delete ALL data!
echo    - Docker containers
echo    - Docker images
echo    - Docker volumes (including database)
echo    - Docker networks
echo.
set /p REPLY="Continue? (yes/no): "

if /i not "%REPLY%"=="yes" (
    echo Cancelled
    exit /b 1
)

echo.
echo ==========================================
echo Step 1: Stopping all containers
echo ==========================================
docker compose -f docker-compose.dev.yml down -v 2>nul
echo Containers stopped

echo.
echo ==========================================
echo Step 2: Removing Docker images
echo ==========================================
docker rmi psychologist-bot-backend 2>nul || echo Backend image not found
docker rmi psychologist-bot-telegram-bot 2>nul || echo Telegram-bot image not found
docker rmi psychologist-bot-frontend 2>nul || echo Frontend image not found
echo Images removed

echo.
echo ==========================================
echo Step 3: Removing Docker volumes
echo ==========================================
docker volume rm psychologist-bot_postgres_dev_data 2>nul || echo Volume postgres_dev_data not found
docker volume rm psychologist-bot_backend_cache 2>nul || echo Volume backend_cache not found
echo Volumes removed

echo.
echo ==========================================
echo Step 4: Removing Docker networks
echo ==========================================
docker network rm psychologist-bot_app-network-dev 2>nul || echo Network not found
echo Networks removed

echo.
echo ==========================================
echo Step 5: Cleaning unused resources
echo ==========================================
docker system prune -f
echo System cleaned

echo.
echo ==========================================
echo Step 6: Building images
echo ==========================================
docker compose -f docker-compose.dev.yml build --no-cache
echo Images built

echo.
echo ==========================================
echo Step 7: Starting containers
echo ==========================================
docker compose -f docker-compose.dev.yml up -d
echo Containers started

echo.
echo ==========================================
echo Step 8: Waiting for services
echo ==========================================
echo Waiting for PostgreSQL...
timeout /t 5 /nobreak >nul
echo Waiting for Backend...
timeout /t 5 /nobreak >nul
echo Waiting for Frontend...
timeout /t 3 /nobreak >nul
echo Waiting for Telegram Bot...
timeout /t 3 /nobreak >nul

echo.
echo ==========================================
echo Step 9: Checking status
echo ==========================================
docker compose -f docker-compose.dev.yml ps

echo.
echo ==========================================
echo DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo Available services:
echo    Backend API:       http://localhost:8000
echo    Frontend:          http://localhost:3000
echo    API Docs:          http://localhost:8000/docs
echo    PgAdmin:           http://localhost:5050
echo    Telegram Bot:      Running
echo.
echo Useful commands:
echo    docker compose -f docker-compose.dev.yml logs -f           # All logs
echo    docker compose -f docker-compose.dev.yml logs backend      # Backend logs
echo    docker compose -f docker-compose.dev.yml logs frontend     # Frontend logs
echo    docker compose -f docker-compose.dev.yml logs telegram-bot # Bot logs
echo    docker compose -f docker-compose.dev.yml ps                # Container status
echo    docker compose -f docker-compose.dev.yml restart frontend  # Restart frontend
echo.
echo Ready to work!
pause
