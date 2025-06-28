@echo off
echo =========================================
echo    Redis Startup (Windows Alternative)
echo =========================================

echo.
echo [1/4] Checking if Redis is already running...
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host 'Redis is already running!' -ForegroundColor Green; exit 0 } catch { Write-Host 'Redis not running, checking options...' -ForegroundColor Yellow }"

if %errorlevel% equ 0 (
    echo Redis is already running on port 6379!
    goto :success
)

echo.
echo [2/4] Checking for Redis Windows installation...
if exist "C:\Program Files\Redis\redis-server.exe" (
    echo Found Redis for Windows installation!
    goto :start_windows_redis
)

REM Check if Redis is installed as a service
sc query Redis >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Redis Windows service!
    goto :start_service
)

echo.
echo [3/4] Redis not found. Checking for Chocolatey...
choco --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Chocolatey found! Installing Redis...
    choco install redis-64 -y
    if %errorlevel% equ 0 goto :start_service
)

echo.
echo [4/4] No Redis installation found.
echo.
echo RECOMMENDED SOLUTION:
echo 1. Download Redis for Windows from:
echo    https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/redis-x64-3.0.504.msi
echo 2. Install it (accept defaults)
echo 3. Run this script again
echo.
echo ALTERNATIVE SOLUTIONS:
echo - Install Chocolatey, then run: choco install redis-64
echo - Fix Docker WSL2 (see DOCKER_ALTERNATIVE.md)
echo.
pause
exit /b 1

:start_windows_redis
echo Starting Redis server manually...
start /b "Redis Server" "C:\Program Files\Redis\redis-server.exe"
timeout /t 3 >nul
goto :test_connection

:start_service
echo Starting Redis Windows service...
net start Redis
if %errorlevel% neq 0 (
    echo Failed to start Redis service. Trying manual start...
    if exist "C:\Program Files\Redis\redis-server.exe" (
        start /b "Redis Server" "C:\Program Files\Redis\redis-server.exe"
        timeout /t 3 >nul
    ) else (
        echo Redis executable not found!
        goto :install_instructions
    )
)

:test_connection
echo.
echo Testing Redis connection...
timeout /t 2 >nul
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host 'SUCCESS: Redis is running!' -ForegroundColor Green } catch { Write-Host 'FAILED: Redis connection test failed' -ForegroundColor Red; exit 1 }"

if %errorlevel% neq 0 (
    echo Connection test failed. Please check the installation.
    pause
    exit /b 1
)

:success
echo.
echo =========================================
echo  🎉 Redis is running on localhost:6379
echo =========================================
echo.
echo You can now start the API server:
echo .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo Or visit: http://localhost:8000/docs
echo.
pause
goto :end

:install_instructions
echo.
echo =========================================
echo        Redis Installation Needed
echo =========================================
echo.
echo Please install Redis for Windows:
echo 1. Download: https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/redis-x64-3.0.504.msi
echo 2. Run the installer
echo 3. Run this script again
echo.
pause

:end
