@echo off
echo =========================================
echo      TEXT-EXTRACT-API Shutdown
echo =========================================

echo.
echo [1/3] Stopping FastAPI server...
echo Please press Ctrl+C in any running FastAPI terminal windows to stop the server.
echo.

echo [2/3] Stopping Redis container (if running via Docker)...
docker stop redis-text-extract >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Redis container stopped
) else (
    echo ℹ️ No Redis container found (may be running as Windows service)
)

echo.
echo [3/3] Stopping Redis Windows service (if installed)...
net stop Redis >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Redis Windows service stopped
) else (
    echo ℹ️ No Redis Windows service found
)

echo.
echo =========================================
echo    All services have been stopped
echo =========================================
echo.
echo To restart everything later:
echo 1. Run: .\start_redis_smart.bat
echo 2. Run: .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
echo.
pause
