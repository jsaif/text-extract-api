# Test Redis Connection
Write-Host "Testing Redis connection..." -ForegroundColor Yellow

try {
    # Test TCP connection to Redis
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect('localhost', 6379)
    $client.Close()
    Write-Host "✅ SUCCESS: Redis is running on localhost:6379" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now start the API server with:" -ForegroundColor Cyan
    Write-Host ".\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload"
} 
catch {
    Write-Host "❌ FAILED: Redis is not running on localhost:6379" -ForegroundColor Red
    Write-Host ""
    Write-Host "To fix this, you need to start Redis:" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if Docker is available
    try {
        $dockerVersion = & docker --version 2>$null
        Write-Host "✅ Docker is available: $dockerVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "Let's start Redis with Docker:" -ForegroundColor Cyan
        Write-Host "1. Make sure Docker Desktop is running (check system tray)"
        Write-Host "2. Run this command:" -ForegroundColor Yellow
        Write-Host "   docker run -d --name redis-text-extract -p 6379:6379 --restart always redis"
        Write-Host ""
        Write-Host "Do you want me to try starting Redis now? (y/n):" -ForegroundColor Cyan -NoNewline
        $response = Read-Host
        if ($response -eq 'y' -or $response -eq 'Y') {
            Write-Host ""
            Write-Host "Starting Redis container..." -ForegroundColor Yellow
            try {
                & docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
                Start-Sleep -Seconds 3
                Write-Host "Checking if Redis started..." -ForegroundColor Yellow
                # Test connection again
                $testClient = New-Object System.Net.Sockets.TcpClient
                $testClient.Connect('localhost', 6379)
                $testClient.Close()
                Write-Host "🎉 SUCCESS! Redis is now running!" -ForegroundColor Green
            }
            catch {
                Write-Host "⚠️ Docker command failed. Please try manually:" -ForegroundColor Red
                Write-Host "docker run -d --name redis-text-extract -p 6379:6379 --restart always redis"
            }
        }
    }
    catch {
        Write-Host "❌ Docker is not available or not in PATH" -ForegroundColor Red
        Write-Host ""
        Write-Host "Alternative Options:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Option 1 - Install Docker Desktop:" -ForegroundColor Cyan
        Write-Host "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        Write-Host ""
        Write-Host "Option 2 - Download Redis for Windows:" -ForegroundColor Cyan
        Write-Host "https://github.com/microsoftarchive/redis/releases"
        Write-Host "Download redis-x64-3.0.504.msi and install it"
        Write-Host ""
        Write-Host "Option 3 - Use Windows Subsystem for Linux (WSL):" -ForegroundColor Cyan
        Write-Host "1. Install WSL: wsl --install"
        Write-Host "2. Install Redis in WSL: sudo apt-get install redis-server"
        Write-Host "3. Start Redis: sudo service redis-server start"
        Write-Host ""
        Write-Host "Option 4 - Use Chocolatey (if installed):" -ForegroundColor Cyan
        Write-Host "choco install redis-64"
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
