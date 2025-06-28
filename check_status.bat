@echo off
echo =========================================
echo     TEXT-EXTRACT-API Status Check
echo =========================================

echo.
echo [1/3] Checking Redis...
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient; $client.Connect('localhost', 6379); $client.Close(); Write-Host '✅ Redis is running on localhost:6379' -ForegroundColor Green } catch { Write-Host '❌ Redis is not running' -ForegroundColor Red }"

echo.
echo [2/3] Checking API Server...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/docs' -UseBasicParsing -TimeoutSec 5; Write-Host '✅ API server is running on http://localhost:8000' -ForegroundColor Green } catch { Write-Host '❌ API server is not running' -ForegroundColor Red }"

echo.
echo [3/3] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is available
    echo Available models:
    ollama list
) else (
    echo ❌ Ollama is not available
)

echo.
echo =========================================
echo           System Status Summary
echo =========================================
echo.
echo If all services are running:
echo 🌐 Web Interface: http://localhost:8000/docs
echo 💻 CLI Usage: .\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf
echo.
pause
