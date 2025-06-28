import pathlib
import sys
import os

from celery import Celery
from dotenv import load_dotenv

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()))

load_dotenv(".env.localhost")

import multiprocessing

multiprocessing.set_start_method("spawn", force=True)

# Get Redis URLs from environment or use localhost defaults
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

app = Celery(
    "text_extract_api",
    broker=broker_url,
    backend=result_backend
)
app.config_from_object({
    "worker_max_memory_per_child": 8200000
})

app.autodiscover_tasks(["text_extract_api.extract"], 'tasks', True)
