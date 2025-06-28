@echo off
cd /d "c:\Users\Jubi\text-extract-api"
call .venv\Scripts\activate.bat
echo Testing Redis connection...
python test_redis.py
echo.
echo Starting FastAPI server...
python -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
pause
