@echo off
echo Installing GPU support for text-extract-api...
echo =============================================

echo.
echo Checking current Python environment...
python --version
echo.

echo Checking for NVIDIA GPU...
where nvidia-smi >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ NVIDIA GPU detected
    nvidia-smi --query-gpu=name --format=csv,noheader,nounits
    
    echo.
    echo Installing PyTorch with CUDA support...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    
    echo.
    echo Installing TensorFlow with GPU support...
    pip install tensorflow[and-cuda]
    
) else (
    echo ❌ No NVIDIA GPU detected
    echo Installing CPU-only versions...
    pip install torch torchvision torchaudio
    pip install tensorflow
)

echo.
echo Installing additional GPU support packages...
pip install -r requirements-gpu.txt

echo.
echo Testing GPU installation...
python -c "import torch; print(f'PyTorch CUDA available: {torch.cuda.is_available()}')"
python -c "import tensorflow as tf; print(f'TensorFlow GPU devices: {len(tf.config.list_physical_devices(\"GPU\"))}')"

echo.
echo GPU setup complete!
echo.
echo To test GPU performance, run:
echo   python test_easyocr_gpu.py
echo   python check_gpu.py
echo.
pause
