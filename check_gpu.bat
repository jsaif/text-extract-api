@echo off
echo GPU Detection and Setup Tool
echo ============================

echo.
echo Checking for NVIDIA GPU...
where nvidia-smi >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ NVIDIA drivers found
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
) else (
    echo ❌ NVIDIA drivers not found
)

echo.
echo Checking for CUDA toolkit...
where nvcc >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ CUDA toolkit found
    nvcc --version | findstr "release"
) else (
    echo ❌ CUDA toolkit not found
)

echo.
echo Running Python GPU detection...
python check_gpu.py

echo.
echo GPU check complete!
pause
