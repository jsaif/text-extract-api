# 🔧 Redis Connection Fix Summary

## Problem
The application was trying to connect to "redis:6379" instead of "localhost:6379", causing connection errors:
```
redis.exceptions.ConnectionError: Error 11001 connecting to redis:6379. getaddrinfo failed.
```

## Root Cause
The application had hardcoded Docker hostnames ("redis") instead of localhost hostnames in:
1. `text_extract_api/main.py` - Redis cache URL default
2. `text_extract_api/celery_app.py` - Celery broker and backend URLs

## What Was Fixed

### 1. Updated main.py
- Added `from dotenv import load_dotenv` and `load_dotenv(".env.localhost")`
- Changed default Redis URL from `redis://redis:6379/1` to `redis://localhost:6379/1`

### 2. Updated celery_app.py
- Added environment variable loading for `.env.localhost`
- Changed hardcoded broker/backend URLs to use environment variables with localhost defaults
- Added `os.getenv()` calls with localhost fallbacks

### 3. Created Helper Scripts
- `start_redis.bat` - Easy Redis container startup
- `start_server.bat` - Easy API server startup
- Updated `USAGE_GUIDE.md` with Redis troubleshooting

## Next Steps
1. **Start Redis**: Run `.\start_redis.bat` or manually start Docker container
2. **Test connection**: Run `test_redis.py` to verify Redis is accessible
3. **Start API server**: Run `.\start_server.bat` or manual uvicorn command
4. **Test the API**: Visit http://localhost:8000/docs

## Files Modified
- `text_extract_api/main.py`
- `text_extract_api/celery_app.py`
- `USAGE_GUIDE.md`
- `start_redis.bat` (new)
- `start_server.bat` (new)

The application should now properly connect to Redis running on localhost instead of trying to find a Docker container named "redis".
