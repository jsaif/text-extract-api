# 🛑 TEXT-EXTRACT-API Shutdown Procedure

## Manual Shutdown Steps:

### 1. Stop FastAPI Server
- **If running in terminal**: Press `Ctrl+C` in the terminal window
- **If running in background**: Close the terminal window

### 2. Stop Redis (Choose based on how you started it)

#### If using Docker:
```cmd
# Stop Redis container
docker stop redis-text-extract

# Optional: Remove container completely
docker rm redis-text-extract
```

#### If using Redis Windows Service:
```cmd
# Stop Redis service
net stop Redis
```

#### If using WSL:
```bash
# In WSL terminal
sudo service redis-server stop
```

### 3. Stop Ollama (Optional)
```cmd
# If you want to stop Ollama too
taskkill /f /im ollama.exe
```

---

## Easy Shutdown Script

**Just run this:**
```cmd
.\shutdown.bat
```

This will automatically stop all services.

---

## ✅ Verification

Check that everything is stopped:
```powershell
# Test if Redis is stopped
.\test_redis_connection.ps1

# Should show: ❌ FAILED: Redis is not running
```

---

## 🔄 To Restart Later

1. **Start Redis**: `.\start_redis_smart.bat`
2. **Start API**: `.\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload`
3. **Test**: Visit http://localhost:8000/docs

---

## 📊 Current Status Summary

✅ **What we accomplished:**
- Fixed Redis connection configuration
- Updated code to use localhost instead of Docker hostnames
- Created startup and testing scripts
- All code is ready to run

❌ **What needs Redis to work:**
- Document processing (requires Redis for Celery task queue)
- API upload endpoints
- Background OCR tasks

💡 **Next time you want to use the API:**
1. Start Redis first
2. Start the API server
3. Process your documents!
