#!/usr/bin/env python3
"""
Quick Redis connection test
"""

import redis
import sys

def test_redis_connection():
    """Test if Redis is accessible"""
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
        r.ping()
        print("✅ Redis is running and accessible!")
        return True
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        print("\n🔧 Fix steps:")
        print("1. Start Docker Desktop")
        print("2. Run: docker run -d --name redis-text-extract -p 6379:6379 --restart always redis")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)
