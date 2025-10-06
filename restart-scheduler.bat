@echo off
REM Restart backend after changing scheduler time (Windows)
REM Usage: restart-scheduler.bat

echo ==========================================
echo Restarting Backend with new scheduler settings
echo ==========================================
echo.

REM Stop and remove backend container
echo Stopping backend...
docker compose -f docker-compose.dev.yml stop backend
docker compose -f docker-compose.dev.yml rm -f backend

echo.
echo Starting backend with new settings...
docker compose -f docker-compose.dev.yml up -d backend

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Checking backend logs:
echo ==========================================
docker compose -f docker-compose.dev.yml logs backend --tail 30 | findstr /i "scheduler morning evening started"

echo.
echo ==========================================
echo Backend restarted!
echo ==========================================
echo.
echo Check scheduler settings in .env file:
echo    MORNING_TASK_TIME
echo    EVENING_REMINDER_TIME
echo.
echo Scheduler will automatically send tasks at specified time
echo For manual sending, use API endpoint:
echo    curl -X POST http://localhost:8000/api/v1/admin/scheduler/send-morning-tasks ^
echo      -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
echo.
pause
