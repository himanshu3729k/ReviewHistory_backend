from app.database import SessionLocal
from app.models import Category, ReviewHistory
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    try:
        # 1. Create Categories
        cat1 = Category(name="Electronics", description="Gadgets and devices")
        cat2 = Category(name="Books", description="Reading materials")
        cat3 = Category(name="Kitchen", description="Cooking tools")
        db.add_all([cat1, cat2, cat3])
        db.commit()

        # 2. Create Reviews with History (Testing the 'Latest' logic)
        # Review A: Version 1 (3 stars) then Version 2 (10 stars)
        rev_a_v1 = ReviewHistory(
            review_id="rev_101", text="Okayish", stars=3, 
            category_id=cat1.id, created_at=datetime.utcnow() - timedelta(days=2)
        )
        rev_a_v2 = ReviewHistory(
            review_id="rev_101", text="Actually great!", stars=10, 
            category_id=cat1.id, created_at=datetime.utcnow()
        )

        # Review B: Single version (5 stars)
        rev_b = ReviewHistory(
            review_id="rev_102", text="Good", stars=5, 
            category_id=cat1.id, created_at=datetime.utcnow()
        )

        db.add_all([rev_a_v1, rev_a_v2, rev_b])
        db.commit()
        print("Database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()