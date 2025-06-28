# 🚀 QUICK START - TEXT EXTRACT API

## Step 1: Start Redis (Choose ONE method)

### Method A: Docker (Recommended)
1. **Start Docker Desktop** from Windows Start Menu
2. **Wait** for Docker Desktop to fully load (look for green status)
3. **Run Redis**:
   ```cmd
   docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
   ```

### Method B: Redis for Windows
1. **Download** Redis from: https://github.com/microsoftarchive/redis/releases
2. **Install** and start Redis service
3. **Verify** it's running on port 6379

### Method C: Windows Subsystem for Linux (WSL)
1. **Install WSL**: `wsl --install`
2. **Install Redis**: `sudo apt-get install redis-server`
3. **Start Redis**: `sudo service redis-server start`

---

## Step 2: Test Redis Connection

Run this PowerShell script to verify Redis is working:
```powershell
.\test_redis_connection.ps1
```

OR run the Python test:
```cmd
.\.venv\Scripts\python.exe test_redis.py
```

---

## Step 3: Start the API Server

```cmd
.\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Step 4: Test the API

Open your browser to: **http://localhost:8000/docs**

---

## ⚠️ Troubleshooting

### "Connection refused" or "10061" error
- Redis is not running
- Follow Step 1 above to start Redis
- Run Step 2 to verify connection

### "Docker not found" error
- Docker Desktop is not installed or not started
- Use Method B or C from Step 1 instead

### "Internal Server Error"
- Check the FastAPI terminal for detailed logs
- Verify Redis is running (Step 2)
- Restart the API server (Step 3)

---

## ✅ Success Indicators

When everything is working, you should see:
1. ✅ Redis connection test passes
2. ✅ API server starts without errors
3. ✅ Web interface loads at http://localhost:8000/docs
4. ✅ Document uploads work without "Internal Server Error"

---

## 📁 Test with Your Documents

Once everything is running:

```cmd
# Process your network testing document
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file "path\to\your\document.pdf" --strategy llama_vision

# Or use the web interface at http://localhost:8000/docs
```
