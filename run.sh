#!/bin/sh

# 1. Force Celery to ignore the root warning safely
export C_FORCE_ROOT="true"

# 2. Run migrations using the cloud database URL
alembic upgrade head

# 3. Start the Celery worker in the background
celery -A app.worker.celery_app worker --loglevel=info --pool=solo &

# 4. Start the FastAPI server in the foreground
uvicorn app.main:app --host 0.0.0.0 --port 8000