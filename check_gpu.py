#!/usr/bin/env python3
"""
GPU Detection and Information Script
Checks for NVIDIA CUDA, AMD ROCm, and Intel GPU support
"""

import sys
import subprocess
import platform

def check_nvidia_gpu():
    """Check for NVIDIA GPU and CUDA support"""
    print("=== NVIDIA GPU Check ===")
    
    # Check nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ NVIDIA GPU detected via nvidia-smi")
            print(result.stdout)
            
            # Try to get CUDA version
            try:
                cuda_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=10)
                if cuda_result.returncode == 0:
                    print("✅ CUDA toolkit installed")
                    print(cuda_result.stdout)
                else:
                    print("⚠️  CUDA toolkit not found in PATH")
            except FileNotFoundError:
                print("⚠️  CUDA toolkit not found")
        else:
            print("❌ No NVIDIA GPU detected or drivers not installed")
            
    except FileNotFoundError:
        print("❌ nvidia-smi not found - NVIDIA drivers may not be installed")
    except subprocess.TimeoutExpired:
        print("⚠️  nvidia-smi timeout")
    except Exception as e:
        print(f"❌ Error checking NVIDIA GPU: {e}")

def check_pytorch_gpu():
    """Check PyTorch GPU support"""
    print("\n=== PyTorch GPU Check ===")
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        # Check CUDA
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.device_count()} device(s)")
            for i in range(torch.cuda.device_count()):
                print(f"   Device {i}: {torch.cuda.get_device_name(i)}")
                print(f"   Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB")
        else:
            print("❌ CUDA not available in PyTorch")
            
        # Check MPS (Apple Silicon)
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("✅ Apple Metal Performance Shaders (MPS) available")
        
    except ImportError:
        print("❌ PyTorch not installed")
    except Exception as e:
        print(f"❌ Error checking PyTorch: {e}")

def check_tensorflow_gpu():
    """Check TensorFlow GPU support"""
    print("\n=== TensorFlow GPU Check ===")
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        
        # Check GPU devices
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ TensorFlow GPU devices: {len(gpus)}")
            for i, gpu in enumerate(gpus):
                print(f"   Device {i}: {gpu}")
                
            # Check if GPU is actually usable
            try:
                with tf.device('/GPU:0'):
                    test_tensor = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                    result = tf.matmul(test_tensor, test_tensor)
                print("✅ GPU computation test passed")
            except Exception as e:
                print(f"⚠️  GPU computation test failed: {e}")
        else:
            print("❌ No GPU devices found in TensorFlow")
            
    except ImportError:
        print("❌ TensorFlow not installed")
    except Exception as e:
        print(f"❌ Error checking TensorFlow: {e}")

def check_system_info():
    """Display system information"""
    print("=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")

def check_opencl():
    """Check OpenCL support"""
    print("\n=== OpenCL Check ===")
    try:
        import pyopencl as cl
        platforms = cl.get_platforms()
        print(f"✅ OpenCL platforms found: {len(platforms)}")
        
        for i, platform in enumerate(platforms):
            print(f"   Platform {i}: {platform.name}")
            devices = platform.get_devices()
            for j, device in enumerate(devices):
                print(f"     Device {j}: {device.name} ({device.type})")
                
    except ImportError:
        print("❌ PyOpenCL not installed")
    except Exception as e:
        print(f"❌ Error checking OpenCL: {e}")

def main():
    """Main function to run all GPU checks"""
    print("🔍 GPU Detection and Information Tool")
    print("=" * 50)
    
    check_system_info()
    check_nvidia_gpu()
    check_pytorch_gpu()
    check_tensorflow_gpu()
    check_opencl()
    
    print("\n" + "=" * 50)
    print("🔍 GPU check complete!")
    print("\nTo install GPU support:")
    print("- PyTorch: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("- TensorFlow: pip install tensorflow[and-cuda]")
    print("- OpenCL: pip install pyopencl")

if __name__ == "__main__":
    main()
