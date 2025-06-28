# 🚨 Docker WSL Error - Alternative Redis Solutions

## Problem
Docker Desktop requires WSL2 and virtualization features that aren't enabled on your machine.

## ✅ EASIEST SOLUTION: Redis for Windows (No Docker Required)

### Step 1: Download Redis for Windows
1. Go to: https://github.com/microsoftarchive/redis/releases
2. Download: **redis-x64-3.0.504.msi**
3. Run the installer (accept all defaults)

### Step 2: Start Redis
```cmd
# Option 1: Start as Windows Service
net start Redis

# Option 2: Start manually
"C:\Program Files\Redis\redis-server.exe"
```

### Step 3: Test Redis
```powershell
.\test_redis_connection.ps1
# Should show: ✅ SUCCESS
```

---

## Alternative Solution: Enable WSL2 (If You Want Docker)

### Step 1: Enable Windows Features
```powershell
# Run PowerShell as Administrator:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# OR use Windows Features GUI:
# 1. Open "Turn Windows features on or off"
# 2. Check "Virtual Machine Platform"
# 3. Check "Windows Subsystem for Linux"
# 4. Restart computer
```

### Step 2: Enable Virtualization in BIOS
1. Restart computer and enter BIOS/UEFI
2. Look for "Intel VT-x" or "AMD-V" or "Virtualization"
3. Enable it
4. Save and restart

### Step 3: Install WSL2
```powershell
# After restart, run as Administrator:
wsl --install --no-distribution
wsl --set-default-version 2
```

---

## ⚡ QUICK FIX: Use Redis for Windows (Recommended)

**This is the simplest solution that doesn't require Docker:**

1. **Download Redis**: https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/redis-x64-3.0.504.msi
2. **Install** (just click through the installer)
3. **Start Redis**:
   ```cmd
   net start Redis
   ```
4. **Test**:
   ```powershell
   .\test_redis_connection.ps1
   ```
5. **Start API**:
   ```cmd
   .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 🛠️ Updated Startup Script

I'll create a new startup script that tries Redis for Windows first, then Docker as fallback.
