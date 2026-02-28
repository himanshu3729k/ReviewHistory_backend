from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    reviews = relationship("ReviewHistory", back_populates="category")

class ReviewHistory(Base):
    __tablename__ = "review_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=True)
    stars = Column(Integer, CheckConstraint('stars >= 1 AND stars <= 10'), nullable=False)
    review_id = Column(String(255), nullable=False)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(BigInteger, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="reviews")

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
