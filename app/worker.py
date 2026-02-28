from celery import Celery
from .database import SessionLocal
from .models import AccessLog

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def log_access_task(log_text: str):
    db = SessionLocal()
    try:
        new_log = AccessLog(text=log_text)
        db.add(new_log)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error logging access: {e}")
    finally:
        db.close()