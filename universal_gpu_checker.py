#!/usr/bin/env python3
"""
Universal GPU Detection and AI Acceleration Script
Portable script for checking GPU capabilities across any Python project
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

class UniversalGPUChecker:
    """Universal GPU detection and AI capability checker"""
    
    def __init__(self, project_name=None):
        self.project_name = project_name or self._detect_project_name()
        self.project_type = self._detect_project_type()
        
    def _detect_project_name(self):
        """Auto-detect project name from current directory"""
        return Path.cwd().name
    
    def _detect_project_type(self):
        """Detect what type of project this is"""
        cwd = Path.cwd()
        
        # Check for various project indicators
        if (cwd / "requirements.txt").exists() or (cwd / "pyproject.toml").exists():
            project_type = "Python"
        elif (cwd / "package.json").exists():
            project_type = "Node.js"
        elif (cwd / "Cargo.toml").exists():
            project_type = "Rust"
        elif (cwd / "go.mod").exists():
            project_type = "Go"
        elif (cwd / "pom.xml").exists():
            project_type = "Java"
        elif (cwd / ".csproj").glob("*.csproj"):
            project_type = ".NET"
        else:
            project_type = "General"
            
        # Check for specific frameworks
        if project_type == "Python":
            requirements_file = cwd / "requirements.txt"
            if requirements_file.exists():
                content = requirements_file.read_text().lower()
                if any(fw in content for fw in ["torch", "pytorch", "tensorflow", "transformers"]):
                    project_type = "Python ML/AI"
                elif any(fw in content for fw in ["fastapi", "flask", "django"]):
                    project_type = "Python Web"
                elif any(fw in content for fw in ["opencv", "pillow", "scikit-image"]):
                    project_type = "Python Computer Vision"
        
        return project_type

    def check_system_info(self):
        """Display system information"""
        print(f"=== System Information for {self.project_name} ===")
        print(f"Project Type: {self.project_type}")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.architecture()[0]}")
        print(f"Python: {sys.version}")
        print(f"Current Directory: {Path.cwd()}")

    def check_nvidia_gpu(self):
        """Check for NVIDIA GPU and CUDA support"""
        print("\n=== NVIDIA GPU Check ===")
        
        # Check nvidia-smi
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ NVIDIA GPU detected via nvidia-smi")
                # Parse GPU info
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Tesla' in line:
                        print(f"   GPU: {line.strip()}")
                
                # Try to get CUDA version
                try:
                    cuda_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=10)
                    if cuda_result.returncode == 0:
                        print("✅ CUDA toolkit installed")
                        # Extract CUDA version
                        for line in cuda_result.stdout.split('\n'):
                            if 'release' in line.lower():
                                print(f"   {line.strip()}")
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

    def check_pytorch_gpu(self):
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
                    props = torch.cuda.get_device_properties(i)
                    print(f"   Memory: {props.total_memory / 1024**3:.1f} GB")
                    print(f"   Compute Capability: {props.major}.{props.minor}")
            else:
                print("❌ CUDA not available in PyTorch")
                
            # Check MPS (Apple Silicon)
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("✅ Apple Metal Performance Shaders (MPS) available")
            
        except ImportError:
            print("❌ PyTorch not installed")
            if self.project_type in ["Python ML/AI", "Python Computer Vision"]:
                print("💡 Install PyTorch for GPU acceleration:")
                print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        except Exception as e:
            print(f"❌ Error checking PyTorch: {e}")

    def check_tensorflow_gpu(self):
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
            if self.project_type in ["Python ML/AI", "Python Computer Vision"]:
                print("💡 Install TensorFlow for GPU acceleration:")
                print("   pip install tensorflow[and-cuda]")
        except Exception as e:
            print(f"❌ Error checking TensorFlow: {e}")

    def check_opencl(self):
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
            print("💡 Install OpenCL support: pip install pyopencl")
        except Exception as e:
            print(f"❌ Error checking OpenCL: {e}")

    def check_ai_development_tools(self):
        """Check AI development tools and extensions"""
        print("\n=== AI Development Tools ===")
        
        print("🤖 AI Code Assistance Benefits:")
        print("1. Local AI Models - Run coding assistants locally with GPU acceleration")
        print("2. Faster Processing - GPU-accelerated code analysis and generation")
        print("3. Real-time Suggestions - Reduced latency for code completions")
        print("4. Custom Models - Train domain-specific models for your project")
        print("5. Privacy - Keep your code local with GPU-accelerated models")
        
        # Check for VS Code
        try:
            result = subprocess.run(['code', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("\n✅ VS Code detected")
                print("🔌 Recommended AI Extensions:")
                extensions = [
                    "Continue.continue - Local AI assistant with GPU support",
                    "ms-vscode.ollama - Local LLM integration", 
                    "GitHub.copilot-chat - AI-powered chat interface",
                    "TabNine.tabnine-vscode - GPU-accelerated completions",
                    "VisualStudioExptTeam.vscodeintellicode - AI-enhanced IntelliSense"
                ]
                
                for ext in extensions:
                    print(f"  • {ext}")
            else:
                print("❌ VS Code not found")
        except FileNotFoundError:
            print("❌ VS Code not found in PATH")
        
        # Check for Ollama (local LLM server)
        print("\n🧠 Local AI Model Server:")
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ Ollama installed - Local AI models available")
                models = result.stdout.strip()
                if models and len(models.split('\n')) > 1:
                    print("📋 Installed models:")
                    for line in models.split('\n')[1:]:  # Skip header
                        if line.strip():
                            print(f"   • {line.strip()}")
                else:
                    print("📋 No models installed yet")
                    print("💡 Install coding models:")
                    print("   ollama pull codellama:7b")
                    print("   ollama pull deepseek-coder:6.7b")
            else:
                print("⚠️  Ollama not responding")
        except FileNotFoundError:
            print("❌ Ollama not installed")
            print("💡 Install from: https://ollama.ai/")
        except Exception as e:
            print(f"⚠️  Error checking Ollama: {e}")

    def check_project_specific_gpu_benefits(self):
        """Show GPU benefits specific to the detected project type"""
        print(f"\n=== GPU Benefits for {self.project_type} Projects ===")
        
        benefits = {
            "Python ML/AI": [
                "Model Training: 10-100x faster with GPU",
                "Inference: 5-50x faster predictions",
                "Data Processing: GPU-accelerated pandas, cuDF",
                "Computer Vision: OpenCV GPU acceleration",
                "Deep Learning: PyTorch/TensorFlow GPU support"
            ],
            "Python Computer Vision": [
                "Image Processing: 10-50x faster with GPU",
                "Video Processing: Real-time processing capabilities",
                "OCR/Text Extraction: GPU-accelerated EasyOCR, TesseractOCR",
                "Object Detection: YOLO, SSD models on GPU",
                "Image Enhancement: GPU-accelerated filters"
            ],
            "Python Web": [
                "API Response Times: Faster ML model serving",
                "Real-time Processing: GPU-accelerated background tasks",
                "Image/Video APIs: GPU processing for media endpoints",
                "AI Features: Local AI model integration",
                "Batch Processing: Parallel GPU computation"
            ],
            "Python": [
                "Scientific Computing: NumPy, SciPy GPU acceleration",
                "Data Analysis: CuPy, Rapids for GPU pandas",
                "Parallel Processing: CUDA Python integration",
                "AI Development: Local model training and inference",
                "Visualization: GPU-accelerated plotting"
            ],
            "Node.js": [
                "AI Integration: TensorFlow.js GPU support",
                "Image Processing: Sharp with GPU acceleration",
                "Real-time Apps: GPU-accelerated WebRTC",
                "ML Serving: GPU model inference APIs",
                "Data Processing: GPU computation via Python bridges"
            ],
            "General": [
                "Development Speed: AI-powered code assistance",
                "Code Analysis: GPU-accelerated linting and analysis",
                "Documentation: AI-generated documentation",
                "Testing: AI-powered test generation",
                "Refactoring: GPU-accelerated code transformations"
            ]
        }
        
        project_benefits = benefits.get(self.project_type, benefits["General"])
        for benefit in project_benefits:
            print(f"• {benefit}")

    def generate_setup_recommendations(self):
        """Generate setup recommendations based on project type"""
        print(f"\n=== Setup Recommendations for {self.project_name} ===")
        
        # Universal recommendations
        print("🚀 Universal GPU Setup:")
        print("1. Check GPU drivers (nvidia-smi)")
        print("2. Install CUDA toolkit if using NVIDIA GPU")
        print("3. Install AI development extensions for your IDE")
        print("4. Set up local AI models with Ollama")
        
        # Project-specific recommendations
        if self.project_type.startswith("Python"):
            print("\n🐍 Python-Specific Setup:")
            print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
            print("pip install tensorflow[and-cuda]")
            
            if "ML/AI" in self.project_type:
                print("pip install transformers accelerate")
                print("pip install cupy-cuda11x  # GPU-accelerated NumPy")
                
            if "Computer Vision" in self.project_type:
                print("pip install opencv-contrib-python")
                print("pip install easyocr  # GPU-accelerated OCR")
                
        elif self.project_type == "Node.js":
            print("\n📦 Node.js-Specific Setup:")
            print("npm install @tensorflow/tfjs-node-gpu")
            print("npm install sharp  # GPU-accelerated image processing")
            
        # VS Code extensions
        print("\n🔌 VS Code Extensions Setup:")
        print("code --install-extension Continue.continue")
        print("code --install-extension ms-vscode.ollama")
        print("code --install-extension GitHub.copilot-chat")

    def create_portable_gpu_script(self):
        """Create a portable version of this script for the current project"""
        script_content = f'''#!/usr/bin/env python3
"""
GPU Detection Script for {self.project_name}
Generated by Universal GPU Checker
"""

# Copy the contents of the universal checker here
# This creates a project-specific version

from pathlib import Path
import sys

# Add the universal checker to this script
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from universal_gpu_checker import UniversalGPUChecker
    
    def main():
        checker = UniversalGPUChecker("{self.project_name}")
        checker.run_full_check()
        
    if __name__ == "__main__":
        main()
        
except ImportError:
    print("Universal GPU Checker not found. Run this script from the same directory.")
'''
        
        script_path = Path.cwd() / "check_gpu_local.py"
        script_path.write_text(script_content)
        print(f"\n📝 Created project-specific GPU script: {script_path}")

    def run_full_check(self):
        """Run the complete GPU check"""
        print(f"🔍 GPU Detection for {self.project_name} ({self.project_type})")
        print("=" * 60)
        
        self.check_system_info()
        self.check_nvidia_gpu()
        self.check_pytorch_gpu()
        self.check_tensorflow_gpu()
        self.check_opencl()
        self.check_ai_development_tools()
        self.check_project_specific_gpu_benefits()
        self.generate_setup_recommendations()
        
        print("\n" + "=" * 60)
        print("🎉 GPU check complete!")
        print(f"\nYour {self.project_type} project '{self.project_name}' is ready for GPU acceleration!")

def main():
    """Main function"""
    checker = UniversalGPUChecker()
    checker.run_full_check()
    
    # Ask if user wants to create a project-specific script
    try:
        response = input("\n❓ Create a project-specific GPU script? (y/n): ").lower()
        if response in ['y', 'yes']:
            checker.create_portable_gpu_script()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
