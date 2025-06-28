# Redis for Windows - Quick Download Links

## Direct Download Links

### Redis for Windows (Recommended)
**Direct Download**: https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/redis-x64-3.0.504.msi

**File Size**: ~3MB  
**Installation**: Simple MSI installer, just accept defaults

### Alternative: Chocolatey Package Manager
If you have Chocolatey installed:
```powershell
# Run as Administrator:
choco install redis-64
```

## Installation Steps

### Method 1: MSI Installer (Easiest)
1. **Download**: Click the direct link above
2. **Run**: Double-click the downloaded .msi file
3. **Install**: Accept all defaults, click Next/Install
4. **Start**: Run `.\start_redis_windows.bat`

### Method 2: Chocolatey (If you have it)
1. **Open PowerShell as Administrator**
2. **Install**: `choco install redis-64`
3. **Start**: Run `.\start_redis_windows.bat`

## After Installation

### Start Redis:
```cmd
# Easy way:
.\start_redis_windows.bat

# Manual way:
net start Redis
```

### Test Redis:
```powershell
.\test_redis_connection.ps1
```

### Start API:
```cmd
.\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Why This is Better Than Docker for Your Case

✅ **No WSL2 required** - Works on any Windows machine  
✅ **No virtualization needed** - No BIOS changes required  
✅ **Smaller footprint** - Redis is only ~3MB vs Docker's ~500MB  
✅ **Faster startup** - Redis starts instantly  
✅ **Native Windows service** - Starts automatically with Windows  

## Troubleshooting

### If Redis won't start:
```cmd
# Check if service exists:
sc query Redis

# Start service manually:
net start Redis

# Or start executable directly:
"C:\Program Files\Redis\redis-server.exe"
```

### If port 6379 is in use:
```cmd
# Check what's using the port:
netstat -an | findstr 6379

# Kill Redis processes:
taskkill /f /im redis-server.exe
```
