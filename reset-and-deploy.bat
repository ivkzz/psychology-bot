@echo off
REM Psychology Bot - Full Reset and Deploy Script for PRODUCTION (Windows)
REM Usage: reset-and-deploy.bat

echo ==========================================
echo Psychology Bot - Production Deployment
echo ==========================================
echo.

echo WARNING: This will delete ALL data and rebuild everything!
echo    - Docker containers
echo    - Docker images
echo    - Docker volumes (including database)
echo    - Docker networks
echo.
echo This will deploy in PRODUCTION mode:
echo    - Optimized builds
echo    - No DevTools
echo    - Production environment variables
echo.
set /p REPLY="Continue? (yes/no): "

if /i not "%REPLY%"=="yes" (
    echo Cancelled
    exit /b 1
)

echo.
echo ==========================================
echo Step 1: Stopping and removing ALL containers
echo ==========================================
echo Stopping all containers...
docker compose down 2>nul
docker compose -f docker-compose.dev.yml down 2>nul
echo.
echo Forcing removal of any remaining psychologist containers...
for /f "tokens=*" %%i in ('docker ps -a -q -f "name=psychologist"') do docker rm -f %%i 2>nul
echo [OK] All containers stopped and removed

echo.
echo ==========================================
echo Step 2: Removing ONLY psychologist-bot Docker images
echo ==========================================
echo Current psychologist-bot images:
docker images | findstr psychologist-bot
echo.
echo Removing psychologist-bot images...
docker rmi psychologist-bot-backend 2>nul && echo [OK] Backend image removed || echo [INFO] Backend image not found
docker rmi psychologist-bot-telegram-bot 2>nul && echo [OK] Telegram-bot image removed || echo [INFO] Telegram-bot image not found
docker rmi psychologist-bot-frontend 2>nul && echo [OK] Frontend image removed || echo [INFO] Frontend image not found
echo [OK] psychologist-bot images removed

echo.
echo ==========================================
echo Step 3: Removing ONLY psychologist-bot Docker volumes
echo ==========================================
echo Current psychologist-bot volumes:
docker volume ls | findstr psychologist-bot
echo.
echo Removing psychologist-bot volumes...
docker volume rm psychologist-bot_postgres_data 2>nul && echo [OK] postgres_data removed || echo [INFO] postgres_data not found
docker volume rm psychologist-bot_postgres_dev_data 2>nul && echo [OK] postgres_dev_data removed || echo [INFO] postgres_dev_data not found
echo [OK] psychologist-bot volumes removed

echo.
echo ==========================================
echo Step 4: Removing ONLY psychologist-bot Docker networks
echo ==========================================
echo Current psychologist-bot networks:
docker network ls | findstr psychologist-bot
echo.
echo Removing psychologist-bot networks...
docker network rm psychologist-bot_app-network 2>nul && echo [OK] app-network removed || echo [INFO] Network not found
docker network rm psychologist-bot_app-network-dev 2>nul && echo [OK] app-network-dev removed || echo [INFO] Network dev not found
docker network rm psychologist-bot_default 2>nul && echo [OK] default network removed || echo [INFO] Default network not found
echo [OK] psychologist-bot networks removed

echo.
echo ==========================================
echo Step 5: Building PRODUCTION images
echo ==========================================
docker compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Failed to build images!
    pause
    exit /b 1
)
echo Production images built

echo.
echo ==========================================
echo Step 6: Starting containers in PRODUCTION mode
echo ==========================================
docker compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start containers!
    pause
    exit /b 1
)
echo Containers started

echo.
echo ==========================================
echo Step 7: Waiting for services
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
echo Step 8: Verifying deployment
echo ==========================================
echo Checking migration status...
docker compose exec -T backend alembic current
echo.
echo Checking database contents...
docker compose exec -T postgres psql -U psychology_user -d psychology_db -c "SELECT COUNT(*) as admin_count FROM users WHERE role = 'ADMIN';" 2>nul
docker compose exec -T postgres psql -U psychology_user -d psychology_db -c "SELECT COUNT(*) as tasks_count FROM tasks;" 2>nul
echo.

echo.
echo ==========================================
echo Step 9: Checking containers status
echo ==========================================
docker compose ps

echo.
echo ==========================================
echo PRODUCTION DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo Available services:
echo    Backend API:       http://localhost:8000
echo    Frontend:          http://localhost:3000
echo    API Docs:          http://localhost:8000/docs
echo    Telegram Bot:      Running
echo.
echo NOTE: This is PRODUCTION mode:
echo    - DevTools are disabled
echo    - Optimized builds
echo    - No hot reload
echo.
echo Database has been reset:
echo    - Fresh PostgreSQL database
echo    - Migrations applied
echo    - Admin user created from .env
echo    - 15 task templates created
echo.
echo Useful commands:
echo    docker compose logs -f           # All logs
echo    docker compose logs backend      # Backend logs
echo    docker compose logs frontend     # Frontend logs
echo    docker compose logs telegram-bot # Bot logs
echo    docker compose ps                # Container status
echo    docker compose restart frontend  # Restart frontend
echo.
echo Ready to work!
pause
