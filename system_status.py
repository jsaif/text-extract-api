#!/usr/bin/env python3
"""
System status check for TEXT-EXTRACT-API
"""

import requests
import redis
import time
import sys

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI server is running")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FastAPI server not accessible: {e}")
        return False

def check_redis():
    """Check if Redis is accessible"""
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis is running and accessible")
        return True
    except Exception as e:
        print(f"❌ Redis not accessible: {e}")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            print(f"✅ Ollama is running with models: {model_names}")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama not accessible: {e}")
        return False

def main():
    print("🔍 TEXT-EXTRACT-API System Status Check\n")
    
    all_good = True
    
    # Check all components
    all_good &= check_api_health()
    all_good &= check_redis()
    all_good &= check_ollama()
    
    print(f"\n{'='*50}")
    if all_good:
        print("🎉 All systems operational!")
        print("\n📚 Ready to process documents:")
        print("• API Documentation: http://localhost:8000/docs")
        print("• Health Check: http://localhost:8000/")
        print("\n🧪 Test with CLI:")
        print(".\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf")
    else:
        print("⚠️ Some components are not running properly")
        print("Please check the setup and restart missing services")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
