from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from datetime import datetime


class CategoryTrend(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    average_stars: float
    total_reviews: int

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    text: Optional[str] = None
    stars: int
    review_id: str
    created_at: datetime
    tone: Optional[str] = None
    sentiment: Optional[str] = None
    category_id: int

    class Config:
        from_attributes = True

