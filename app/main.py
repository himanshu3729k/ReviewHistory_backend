from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List
from datetime import datetime

from . import models, schemas
from .database import get_db
from .worker import log_access_task
from .llm_service import analyze_review_sentiment

app = FastAPI(title="Review Backend Service")

@app.get("/reviews/trends", response_model=List[schemas.CategoryTrend])
def get_trends(db: Session = Depends(get_db)):
    # Asynchronously log the access [cite: 38, 40]
    log_access_task.delay("GET /reviews/trends")
    
    # Subquery to find the latest version (id) for each unique review_id [cite: 30, 31]
    latest_rev_sub = (
        db.query(models.ReviewHistory)
        .distinct(models.ReviewHistory.review_id)
        .order_by(models.ReviewHistory.review_id, models.ReviewHistory.created_at.desc())
        .subquery()
    )

    # Calculate top 5 categories by avg stars of latest reviews [cite: 27, 29]
    results = (
        db.query(
            models.Category.id,
            models.Category.name,
            models.Category.description,
            func.avg(latest_rev_sub.c.stars).label("average_stars"),
            func.count(latest_rev_sub.c.id).label("total_reviews")
        )
        .join(latest_rev_sub, models.Category.id == latest_rev_sub.c.category_id)
        .group_by(models.Category.id)
        .order_by(func.avg(latest_rev_sub.c.stars).desc())
        .limit(5)
        .all()
    )
    return results

@app.get("/reviews/", response_model=List[schemas.ReviewResponse])
def get_category_reviews(
    category_id: int = Query(...),
    cursor: datetime = Query(None),
    db: Session = Depends(get_db)
):
    # Asynchronously log the access [cite: 57, 59]
    log_access_task.delay(f"GET /reviews/?category_id={category_id}")

    # Identify latest versions for the specific category [cite: 42, 43]
    latest_rev_sub = (
        db.query(models.ReviewHistory)
        .filter(models.ReviewHistory.category_id == category_id)
        .distinct(models.ReviewHistory.review_id)
        .order_by(models.ReviewHistory.review_id, models.ReviewHistory.created_at.desc())
        .subquery()
    )
    
    LatestReview = aliased(models.ReviewHistory, latest_rev_sub)
    query = db.query(LatestReview)

    # Cursor Pagination (Page size: 15) [cite: 42, 44]
    if cursor:
        query = query.filter(LatestReview.created_at < cursor)
    
    reviews = query.order_by(LatestReview.created_at.desc()).limit(15).all()

    # Fill missing tone/sentiment using LLM [cite: 56]
    for rev in reviews:
        if rev.tone is None or rev.sentiment is None:
            t, s = analyze_review_sentiment(rev.text, rev.stars)
            rev.tone, rev.sentiment = t, s
            db.add(rev)
    
    db.commit()
    return reviews