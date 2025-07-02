#!/usr/bin/env python3
"""
Simple GPU Status Check for text-extract-api
"""

def check_gpu_status():
    """Check current GPU capabilities for text extraction"""
    print("🔍 GPU Status for Text-Extract-API")
    print("=" * 40)
    
    # Check system GPU
    print("\n📱 System GPU Information:")
    try:
        import subprocess
        result = subprocess.run(['powershell', 'Get-WmiObject -Class Win32_VideoController | Select-Object Name'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Could not detect system GPU")
    except Exception as e:
        print(f"Error checking system GPU: {e}")
    
    # Check EasyOCR GPU capability
    print("\n🔤 EasyOCR GPU Support:")
    try:
        import easyocr
        print(f"✅ EasyOCR version: {easyocr.__version__}")
        
        # Try GPU initialization
        try:
            reader = easyocr.Reader(['en'], gpu=True, verbose=False)
            print("✅ GPU reader initialization: SUCCESS")
            gpu_available = True
        except Exception as e:
            print(f"❌ GPU reader failed: {e}")
            gpu_available = False
        
        # Try CPU initialization
        try:
            reader_cpu = easyocr.Reader(['en'], gpu=False, verbose=False)
            print("✅ CPU reader initialization: SUCCESS")
        except Exception as e:
            print(f"❌ CPU reader failed: {e}")
            
    except ImportError:
        print("❌ EasyOCR not installed")
        gpu_available = False
    
    # Check PyTorch
    print("\n🔥 PyTorch GPU Support:")
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA devices: {torch.cuda.device_count()}")
            print(f"Current device: {torch.cuda.get_device_name()}")
    except ImportError:
        print("❌ PyTorch not installed")
    
    # Check TensorFlow
    print("\n🤖 TensorFlow GPU Support:")
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        gpus = tf.config.list_physical_devices('GPU')
        print(f"GPU devices detected: {len(gpus)}")
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"  GPU {i}: {gpu}")
    except ImportError:
        print("❌ TensorFlow not installed")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not gpu_available:
        print("• Currently running in CPU mode")
        print("• For GPU acceleration, you need:")
        print("  - NVIDIA GPU with CUDA support")
        print("  - CUDA drivers installed")
        print("  - Run: install_gpu_support.bat")
    else:
        print("• GPU acceleration is available!")
        print("• Use 'easyocr_gpu' strategy for faster processing")
    
    print("\n🚀 Available Strategies:")
    print("• easyocr - Standard CPU-based OCR")
    print("• easyocr_gpu - GPU-accelerated OCR (when available)")
    print("• docling - Document parsing")
    print("• ollama - AI-powered extraction")

if __name__ == "__main__":
    check_gpu_status()
