#!/usr/bin/env python3
"""
Verification script to check if all key dependencies are installed properly.
"""

import sys
import importlib

required_packages = [
    'fastapi',
    'easyocr', 
    'celery',
    'redis',
    'cv2',  # opencv-python-headless
    'pdf2image',
    'ollama',
    'uvicorn',
    'requests',
    'PIL',  # Pillow
    'magic',  # python-magic
    'yaml',  # PyYAML
    'boto3',
    'numpy',
    'pydantic',
    'dotenv',  # python-dotenv
    'docling',
    'transformers'
]

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking TEXT-EXTRACT-API dependencies...\n")
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            installed_packages.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    print(f"\n📊 Summary:")
    print(f"✅ Installed: {len(installed_packages)}")
    print(f"❌ Missing: {len(missing_packages)}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print(f"\n💡 Run: pip install {' '.join(missing_packages)}")
        return False
    else:
        print(f"\n🎉 All dependencies are installed successfully!")
        return True

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)
