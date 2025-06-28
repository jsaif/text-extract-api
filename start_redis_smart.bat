@echo off
echo =========================================
echo      Redis Quick Start Script
echo =========================================

echo.
echo [1/3] Checking if Redis is already running...
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host 'Redis is already running!' -ForegroundColor Green; exit 0 } catch { Write-Host 'Redis not running, starting...' -ForegroundColor Yellow }"

if %errorlevel% equ 0 (
    echo Redis is already running on port 6379!
    goto :success
)

echo.
echo [2/3] Checking for Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker not found. Checking for installed Redis...
    
    REM Check if Redis is installed as a Windows service
    sc query Redis >nul 2>&1
    if %errorlevel% equ 0 (
        echo Found Redis Windows service. Starting...
        net start Redis
        goto :test_connection
    )
    
    echo No Redis installation found.
    echo.
    echo Please install Redis using one of these methods:
    echo.
    echo 1. Docker Desktop: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
    echo 2. Redis for Windows: https://github.com/microsoftarchive/redis/releases
    echo 3. Chocolatey: choco install redis-64
    echo 4. WSL: wsl --install, then sudo apt-get install redis-server
    echo.
    pause
    exit /b 1
)

echo [OK] Docker found!
echo.
echo [3/3] Starting Redis container...

REM Try to start existing container first
docker start redis-text-extract >nul 2>&1
if %errorlevel% equ 0 (
    echo Existing Redis container started!
) else (
    echo Creating new Redis container...
    docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
    if %errorlevel% neq 0 (
        echo Failed to start Redis container.
        echo Please make sure Docker Desktop is running.
        pause
        exit /b 1
    )
)

:test_connection
echo.
echo Testing connection...
timeout /t 3 >nul
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host 'SUCCESS: Redis is running!' -ForegroundColor Green } catch { Write-Host 'FAILED: Redis connection test failed' -ForegroundColor Red; exit 1 }"

if %errorlevel% neq 0 (
    echo Connection test failed. Please check the logs above.
    pause
    exit /b 1
)

:success
echo.
echo =========================================
echo  🎉 Redis is now running on localhost:6379
echo =========================================
echo.
echo You can now start the API server:
echo .venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
echo.
pause
