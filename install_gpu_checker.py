#!/usr/bin/env python3
"""
Portable GPU Checker Installer
Copies GPU detection scripts to any project directory
"""

import shutil
import sys
from pathlib import Path
import argparse

def install_gpu_checker(target_dir=None, project_name=None):
    """Install GPU checker in target directory"""
    
    if target_dir is None:
        target_dir = input("Enter target project directory (or press Enter for current): ").strip()
        if not target_dir:
            target_dir = "."
    
    target_path = Path(target_dir).resolve()
    
    if not target_path.exists():
        print(f"❌ Directory {target_path} does not exist")
        return False
    
    print(f"📁 Installing GPU checker in: {target_path}")
    
    # Copy the universal checker
    source_files = [
        "universal_gpu_checker.py",
        "check_gpu.py"  # Original script as backup
    ]
    
    current_dir = Path(__file__).parent
    
    for file_name in source_files:
        source_file = current_dir / file_name
        if source_file.exists():
            target_file = target_path / file_name
            shutil.copy2(source_file, target_file)
            print(f"✅ Copied {file_name}")
        else:
            print(f"⚠️  {file_name} not found in current directory")
    
    # Create a simple runner script
    runner_content = f'''#!/usr/bin/env python3
"""
GPU Detection for {project_name or target_path.name}
Simple runner script
"""

try:
    from universal_gpu_checker import UniversalGPUChecker
    
    def main():
        checker = UniversalGPUChecker("{project_name or target_path.name}")
        checker.run_full_check()
    
    if __name__ == "__main__":
        main()
        
except ImportError:
    print("❌ universal_gpu_checker.py not found in this directory")
    print("💡 Run the installer again or copy the file manually")
'''
    
    runner_file = target_path / "gpu_check.py"
    runner_file.write_text(runner_content)
    print(f"✅ Created runner script: gpu_check.py")
    
    # Create batch file for Windows
    batch_content = f'''@echo off
echo GPU Detection for {project_name or target_path.name}
echo ================{"=" * len(project_name or target_path.name)}
python gpu_check.py
pause
'''
    
    batch_file = target_path / "gpu_check.bat"
    batch_file.write_text(batch_content)
    print(f"✅ Created Windows batch file: gpu_check.bat")
    
    # Create setup instructions
    readme_content = f'''# GPU Detection Setup for {project_name or target_path.name}

## Quick Start
```bash
# Run GPU detection
python gpu_check.py

# Windows users can double-click
gpu_check.bat
```

## What was installed
- `universal_gpu_checker.py` - Main GPU detection library
- `gpu_check.py` - Simple runner for this project
- `gpu_check.bat` - Windows batch file
- `check_gpu.py` - Original detailed checker

## Features
- ✅ Auto-detects project type ({target_path.name})
- ✅ NVIDIA CUDA detection
- ✅ PyTorch/TensorFlow GPU support
- ✅ AI development tools check
- ✅ Project-specific GPU benefits
- ✅ Setup recommendations

## Usage in other projects
Copy these files to any Python project directory and run `python gpu_check.py`

## GPU Benefits for Your Project Type
The script automatically detects your project type and shows relevant GPU acceleration benefits.

Enjoy GPU-accelerated development! 🚀
'''
    
    readme_file = target_path / "GPU_DETECTION_README.md"
    readme_file.write_text(readme_content)
    print(f"✅ Created documentation: GPU_DETECTION_README.md")
    
    print(f"\n🎉 GPU checker installed successfully!")
    print(f"📍 Location: {target_path}")
    print(f"\n🚀 To use:")
    print(f"   cd {target_path}")
    print(f"   python gpu_check.py")
    
    return True

def main():
    """Main installer function"""
    parser = argparse.ArgumentParser(description="Install portable GPU checker")
    parser.add_argument("--target", "-t", help="Target directory")
    parser.add_argument("--name", "-n", help="Project name")
    parser.add_argument("--list-projects", "-l", action="store_true", 
                       help="List suggested project directories")
    
    args = parser.parse_args()
    
    if args.list_projects:
        print("🔍 Scanning for potential project directories...")
        current = Path.cwd()
        
        # Look for common project indicators
        potential_projects = []
        
        for item in current.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                indicators = [
                    item / "requirements.txt",
                    item / "package.json", 
                    item / "pyproject.toml",
                    item / "Cargo.toml",
                    item / "go.mod"
                ]
                
                if any(ind.exists() for ind in indicators):
                    potential_projects.append(item)
        
        if potential_projects:
            print("📋 Found potential projects:")
            for i, proj in enumerate(potential_projects, 1):
                print(f"   {i}. {proj.name} ({proj})")
            
            try:
                choice = input("\nSelect project number (or Enter to skip): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(potential_projects):
                        target = potential_projects[idx]
                        install_gpu_checker(str(target), target.name)
                        return
            except (ValueError, KeyboardInterrupt):
                pass
        
        print("No automatic selection made.")
    
    # Manual installation
    install_gpu_checker(args.target, args.name)

if __name__ == "__main__":
    main()
