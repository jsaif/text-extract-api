@echo off
echo =========================================
echo         Redis Startup Script
echo =========================================

echo.
echo Checking Docker Desktop status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not available or not in PATH.
    echo.
    echo Please try one of these options:
    echo.
    echo 1. Start Docker Desktop manually:
    echo    - Open Docker Desktop from Start Menu
    echo    - Wait for it to fully start
    echo    - Then run this script again
    echo.
    echo 2. Download Docker Desktop:
    echo    https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
    echo.
    echo 3. Alternative: Install Redis for Windows:
    echo    https://github.com/microsoftarchive/redis/releases
    echo.
    echo 4. Use Windows Subsystem for Linux (WSL) with Redis
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is available!
echo.

echo Checking if Redis container already exists...
docker ps -a | findstr redis-text-extract >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Redis container exists. Starting it...
    docker start redis-text-extract
) else (
    echo [INFO] Creating new Redis container...
    docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
)

echo.
echo Checking Redis container status...
docker ps | findstr redis

echo.
echo Testing Redis connection...
timeout /t 3 >nul
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host '[OK] Redis is responding on localhost:6379' -ForegroundColor Green } catch { Write-Host '[ERROR] Redis is not responding' -ForegroundColor Red }"

echo.
echo =========================================
echo Redis should now be available at localhost:6379
echo You can now run the API server!
echo =========================================
pause
