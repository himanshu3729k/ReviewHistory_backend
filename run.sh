#!/bin/sh

# 1. Run migrations automatically on startup
alembic upgrade head

# 2. Start the Celery worker in the background (&)
# We use --pool=solo because it's more stable in low-memory free environments
celery -A app.worker.celery_app worker --loglevel=info --pool=solo &

# 3. Start the FastAPI server in the foreground
uvicorn app.main:app --host 0.0.0.0 --port 8000