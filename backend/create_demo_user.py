"""
Script to create demo user for the DR Detection System
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User
from app.services.auth import get_password_hash

def create_demo_user():
    """Create demo user if it doesn't exist"""
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "demo@demo.com").first()
        
        if demo_user:
            print("Demo user already exists!")
            print(f"Email: {demo_user.email}")
            print(f"Name: {demo_user.name}")
            print(f"Role: {demo_user.role}")
            return
        
        # Create demo user
        hashed_password = get_password_hash("Demo@123")
        demo_user = User(
            email="demo@demo.com",
            name="Demo User",
            hashed_password=hashed_password,
            role="patient"
        )
        
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        print("✓ Demo user created successfully!")
        print(f"Email: demo@demo.com")
        print(f"Password: Demo@123")
        print(f"Name: {demo_user.name}")
        print(f"Role: {demo_user.role}")
        
    except Exception as e:
        print(f"Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
