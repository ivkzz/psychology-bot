@echo off
REM Psychology Bot - Database Reset Script (Windows)
REM Usage: reset-database.bat [--auto-confirm]
REM This script resets the database and rebuilds images with --no-cache
REM Parameter: --auto-confirm - Skip confirmation prompt (for use in other scripts)

echo ==========================================
echo Psychology Bot - Database Reset
echo ==========================================
echo.

REM Check if --auto-confirm parameter is passed
if "%1"=="--auto-confirm" (
    echo Running in auto-confirm mode...
    goto :skip_confirmation
)

echo WARNING: This will delete ALL database data!
echo    - All users (except admin from .env)
echo    - All tasks assignments
echo    - All user progress
echo.
echo The following will be rebuilt:
echo    - Docker images (with --no-cache to include latest code)
echo    - Task templates (will be recreated from migration)
echo    - Admin user (will be recreated from .env)
echo.
set /p REPLY="Continue? (yes/no): "

if /i not "%REPLY%"=="yes" (
    echo Cancelled
    exit /b 1
)

:skip_confirmation

echo.
echo ==========================================
echo Step 1: Stopping and removing containers
echo ==========================================
echo Stopping all containers...
docker compose down 2>nul
docker compose -f docker-compose.dev.yml down 2>nul
echo.
echo Forcing removal of any remaining psychologist containers...
for /f "tokens=*" %%i in ('docker ps -a -q -f "name=psychologist"') do docker rm -f %%i 2>nul
echo Containers stopped and removed

echo.
echo ==========================================
echo Step 2: Removing ONLY psychologist-bot database volumes
echo ==========================================
echo Current psychologist volumes:
docker volume ls | findstr psychologist-bot
echo.
echo Removing psychologist-bot volumes...
docker volume rm psychologist-bot_postgres_data 2>nul && echo [OK] postgres_data removed || echo [INFO] postgres_data not found
docker volume rm psychologist-bot_postgres_dev_data 2>nul && echo [OK] postgres_dev_data removed || echo [INFO] postgres_dev_data not found
echo.
echo Final verification - remaining psychologist-bot volumes:
docker volume ls | findstr psychologist-bot 2>nul && echo [WARNING] Some volumes still exist! || echo [OK] All psychologist-bot volumes removed successfully

echo.
echo ==========================================
echo Step 3: Removing old Docker images
echo ==========================================
echo Removing psychologist-bot images...
docker rmi psychologist-bot-backend 2>nul && echo [OK] Backend image removed || echo [INFO] Backend image not found
docker rmi psychologist-bot-telegram-bot 2>nul && echo [OK] Telegram-bot image removed || echo [INFO] Telegram-bot image not found
docker rmi psychologist-bot-frontend 2>nul && echo [OK] Frontend image removed || echo [INFO] Frontend image not found
echo [OK] Old images removed

echo.
echo ==========================================
echo Step 4: Rebuilding images without cache
echo ==========================================
echo Building fresh images...
docker compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Failed to build images!
    pause
    exit /b 1
)
echo [OK] Images rebuilt

echo.
echo ==========================================
echo Step 5: Starting containers
echo ==========================================
docker compose up -d
echo Containers started

echo.
echo ==========================================
echo Step 6: Waiting for services
echo ==========================================
echo Waiting for PostgreSQL to initialize...
timeout /t 10 /nobreak >nul
echo Waiting for Backend to apply migrations...
timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo Step 7: Verifying database reset
echo ==========================================
echo Checking migration status...
docker compose exec -T backend alembic current
echo.
echo Checking database contents...
echo.
echo Admin users:
docker compose exec -T postgres psql -U psychology_user -d psychology_db -c "SELECT name, email, role FROM users WHERE role = 'ADMIN';"
echo.
echo Task templates:
docker compose exec -T postgres psql -U psychology_user -d psychology_db -c "SELECT COUNT(*) as tasks_count FROM tasks;"
echo.
echo User assignments:
docker compose exec -T postgres psql -U psychology_user -d psychology_db -c "SELECT COUNT(*) as assignments_count FROM assignments;"

echo.
echo ==========================================
echo Step 8: Checking containers status
echo ==========================================
docker compose ps

echo.
echo ==========================================
echo DATABASE RESET COMPLETE!
echo ==========================================
echo.
echo Database has been reset to initial state:
echo    ✓ Fresh database with empty tables
echo    ✓ Migrations applied (current version)
echo    ✓ Admin user created from .env
echo    ✓ 15 task templates created
echo    ✓ No user data or assignments
echo.
echo Available services:
echo    Backend API:       http://localhost:8000
echo    Frontend:          http://localhost:3000
echo    API Docs:          http://localhost:8000/docs
echo.
echo You can now:
echo    1. Login to admin panel with credentials from .env
echo    2. Register test users via Telegram bot
echo    3. Assign tasks to users
echo.
pause
