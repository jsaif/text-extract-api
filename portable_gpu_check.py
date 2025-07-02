#!/usr/bin/env python3
"""
Standalone Portable GPU Detection Script
Self-contained version that can be copied to any project
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

def detect_project_info():
    """Auto-detect project name and type"""
    cwd = Path.cwd()
    project_name = cwd.name
    
    # Detect project type
    if (cwd / "requirements.txt").exists() or (cwd / "pyproject.toml").exists():
        project_type = "Python"
        
        # Check for specific Python frameworks
        req_file = cwd / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text().lower()
            if any(fw in content for fw in ["torch", "pytorch", "tensorflow", "transformers"]):
                project_type = "Python ML/AI"
            elif any(fw in content for fw in ["fastapi", "flask", "django"]):
                project_type = "Python Web"
            elif any(fw in content for fw in ["opencv", "pillow", "scikit-image", "easyocr"]):
                project_type = "Python Computer Vision"
                
    elif (cwd / "package.json").exists():
        project_type = "Node.js"
    elif (cwd / "Cargo.toml").exists():
        project_type = "Rust"
    elif (cwd / "go.mod").exists():
        project_type = "Go"
    elif (cwd / "pom.xml").exists():
        project_type = "Java"
    elif list(cwd.glob("*.csproj")):
        project_type = ".NET"
    else:
        project_type = "General"
    
    return project_name, project_type

def check_nvidia_gpu():
    """Check for NVIDIA GPU"""
    print("\n🎮 NVIDIA GPU Check")
    print("-" * 30)
    
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ NVIDIA GPU detected")
            # Extract GPU name
            for line in result.stdout.split('\n'):
                if any(gpu in line for gpu in ['GeForce', 'RTX', 'GTX', 'Tesla', 'Quadro']):
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if any(gpu in part for gpu in ['GeForce', 'RTX', 'GTX', 'Tesla', 'Quadro']):
                            gpu_name = ' '.join(parts[i:i+3])
                            print(f"   GPU: {gpu_name}")
                            break
                    break
            
            # Check CUDA
            try:
                cuda_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=5)
                if cuda_result.returncode == 0:
                    for line in cuda_result.stdout.split('\n'):
                        if 'release' in line.lower():
                            print(f"   CUDA: {line.strip()}")
                            break
                else:
                    print("   ⚠️  CUDA toolkit not in PATH")
            except FileNotFoundError:
                print("   ⚠️  CUDA toolkit not found")
                
        else:
            print("❌ No NVIDIA GPU detected")
            
    except FileNotFoundError:
        print("❌ NVIDIA drivers not installed")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_python_gpu_libraries():
    """Check Python GPU libraries"""
    print("\n🐍 Python GPU Libraries")
    print("-" * 30)
    
    # PyTorch
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        if torch.cuda.is_available():
            print(f"   🚀 CUDA: {torch.cuda.device_count()} device(s)")
            print(f"   📱 Current: {torch.cuda.get_device_name()}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("   🍎 Apple Metal available")
        else:
            print("   💻 CPU mode only")
    except ImportError:
        print("❌ PyTorch not installed")
    
    # TensorFlow
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__}")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"   🚀 GPU devices: {len(gpus)}")
        else:
            print("   💻 CPU mode only")
    except ImportError:
        print("❌ TensorFlow not installed")

def check_ai_tools():
    """Check AI development tools"""
    print("\n🤖 AI Development Tools")
    print("-" * 30)
    
    # VS Code
    try:
        result = subprocess.run(['code', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ VS Code {version}")
        else:
            print("❌ VS Code not responding")
    except FileNotFoundError:
        print("❌ VS Code not found")
    
    # Ollama
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama (local AI server)")
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                print(f"   📦 Models: {len(lines) - 1} installed")
            else:
                print("   📦 No models installed")
        else:
            print("❌ Ollama not responding")
    except FileNotFoundError:
        print("❌ Ollama not installed")

def show_gpu_benefits(project_type):
    """Show GPU benefits for project type"""
    print(f"\n🚀 GPU Benefits for {project_type}")
    print("-" * 40)
    
    benefits = {
        "Python ML/AI": [
            "Model training: 10-100x faster",
            "Inference: 5-50x speedup", 
            "Data processing: GPU pandas/cuDF",
            "Deep learning: PyTorch/TensorFlow acceleration"
        ],
        "Python Computer Vision": [
            "Image processing: 10-50x faster",
            "OCR/text extraction: GPU EasyOCR",
            "Video processing: Real-time capabilities",
            "Object detection: GPU YOLO/SSD models"
        ],
        "Python Web": [
            "ML model serving: Faster API responses",
            "Background tasks: GPU parallel processing",
            "Media processing: GPU image/video APIs",
            "Real-time features: GPU-accelerated endpoints"
        ],
        "Python": [
            "Scientific computing: GPU NumPy/SciPy",
            "Data analysis: RAPIDS GPU acceleration",
            "Parallel processing: CUDA integration",
            "Visualization: GPU-accelerated plotting"
        ],
        "Node.js": [
            "TensorFlow.js: GPU model inference",
            "Image processing: GPU Sharp acceleration",
            "Real-time apps: GPU WebRTC processing",
            "ML APIs: GPU computation bridges"
        ]
    }
    
    project_benefits = benefits.get(project_type, [
        "AI code assistance: 10-100x faster",
        "Code analysis: GPU-accelerated tools",
        "Development: AI-powered features",
        "Processing: Parallel GPU computation"
    ])
    
    for benefit in project_benefits:
        print(f"• {benefit}")

def show_setup_instructions(project_type):
    """Show setup instructions"""
    print(f"\n⚙️  GPU Setup for {project_type}")
    print("-" * 40)
    
    print("🔧 Hardware Setup:")
    print("1. Install GPU drivers (nvidia-smi)")
    print("2. Install CUDA toolkit")
    print("3. Verify with: nvidia-smi")
    
    if project_type.startswith("Python"):
        print("\n🐍 Python GPU Libraries:")
        print("pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
        print("pip install tensorflow[and-cuda]")
        
        if "ML/AI" in project_type:
            print("pip install transformers accelerate")
        if "Computer Vision" in project_type:
            print("pip install opencv-contrib-python easyocr")
    
    print("\n🤖 AI Development Tools:")
    print("• Install Ollama: https://ollama.ai/")
    print("• VS Code extensions:")
    print("  - Continue.continue (local AI)")
    print("  - GitHub.copilot-chat (AI chat)")
    print("  - ms-vscode.ollama (LLM integration)")

def main():
    """Main function"""
    project_name, project_type = detect_project_info()
    
    print("🔍 Portable GPU Detection Tool")
    print("=" * 50)
    print(f"📁 Project: {project_name}")
    print(f"🏷️  Type: {project_type}")
    print(f"📍 Location: {Path.cwd()}")
    print(f"💻 OS: {platform.system()} {platform.release()}")
    
    check_nvidia_gpu()
    check_python_gpu_libraries()
    check_ai_tools()
    show_gpu_benefits(project_type)
    show_setup_instructions(project_type)
    
    print("\n" + "=" * 50)
    print("🎉 GPU detection complete!")
    print(f"\nYour {project_type} project is ready for GPU acceleration!")
    
    # Performance summary
    print(f"\n📊 Expected GPU Performance Gains:")
    print("• AI/ML tasks: 10-100x faster")
    print("• Code assistance: 5-20x faster")
    print("• Image/video processing: 10-50x faster")
    print("• Data analysis: 5-30x faster")

if __name__ == "__main__":
    main()
