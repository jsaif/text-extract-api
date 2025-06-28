# 🚨 CURRENT STATUS: Redis Not Running

## ✅ What's Working:
- TEXT-EXTRACT-API code is fixed and ready
- Configuration points to correct localhost:6379
- All dependencies are installed
- Ollama models are available

## ❌ What's Missing:
- **Redis server is not running on port 6379**

---

# 🔧 SOLUTIONS (Pick One)

## Option 1: Docker Desktop (Recommended)

### Step 1: Install Docker Desktop
- Download: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
- Install and restart your computer if needed
- Start Docker Desktop from Start Menu
- Wait for Docker to show "Running" status

### Step 2: Start Redis
```cmd
# Run this command:
docker run -d --name redis-text-extract -p 6379:6379 --restart always redis

# Or use our smart script:
.\start_redis_smart.bat
```

---

## Option 2: Redis for Windows (Direct Install)

### Step 1: Download Redis
- Go to: https://github.com/microsoftarchive/redis/releases
- Download: `redis-x64-3.0.504.msi`
- Install it

### Step 2: Start Redis Service
```cmd
# Start Redis as Windows service:
net start Redis

# Or start manually:
redis-server
```

---

## Option 3: Windows Subsystem for Linux (WSL)

### Step 1: Install WSL
```powershell
# Run as Administrator:
wsl --install
# Restart computer when prompted
```

### Step 2: Install Redis in WSL
```bash
# In WSL terminal:
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
```

---

## Option 4: Chocolatey (If You Have It)

```powershell
# Run as Administrator:
choco install redis-64
redis-server
```

---

# 🧪 TEST YOUR SOLUTION

After starting Redis with any method above:

```powershell
# Test Redis connection:
.\test_redis_connection.ps1

# Should show: ✅ SUCCESS: Redis is running on localhost:6379
```

---

# 🚀 ONCE REDIS IS RUNNING

## Start the API Server:
```cmd
.\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Open Web Interface:
http://localhost:8000/docs

## Process Your Document:
```cmd
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file "your-document.pdf" --strategy llama_vision
```

---

# 📞 QUICK HELP

**If you see "connection refused" errors:**
- Redis is not running → Start Redis using one of the options above

**If you see "Docker not found" errors:**
- Install Docker Desktop or use Option 2/3/4 instead

**If Redis starts but connection still fails:**
- Check Windows Firewall
- Try restarting your terminal
- Run: `netstat -an | findstr 6379` to see if port is in use

---

## 💡 RECOMMENDED NEXT STEP:

1. **Try Docker first** (Option 1) - it's the most reliable
2. **If Docker doesn't work**, use Redis for Windows (Option 2)
3. **Test with**: `.\test_redis_connection.ps1`
4. **When Redis works**, start the API server and test your documents!
