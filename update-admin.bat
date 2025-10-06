@echo off
REM Update admin user credentials from .env file
REM Usage: update-admin.bat

echo ==========================================
echo Updating Admin Credentials
echo ==========================================
echo.
echo This will update admin user with values from .env file:
echo.

REM Show current .env values
findstr /C:"ADMIN_EMAIL" .env
findstr /C:"ADMIN_NAME" .env
echo ADMIN_PASSWORD: [hidden]
echo.

set /p REPLY="Continue? (yes/no): "

if /i not "%REPLY%"=="yes" (
    echo Cancelled
    exit /b 1
)

echo.
echo Running update script...
docker compose -f docker-compose.dev.yml exec backend python scripts/update_admin.py

echo.
echo Done!
pause
