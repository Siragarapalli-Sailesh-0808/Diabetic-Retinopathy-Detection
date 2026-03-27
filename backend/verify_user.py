"""
Script to verify and update demo user credentials
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User
from app.services.auth import get_password_hash, verify_password

def verify_demo_user():
    """Verify demo user credentials"""
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Get demo user
        demo_user = db.query(User).filter(User.email == "demo@demo.com").first()
        
        if not demo_user:
            print("Demo user not found!")
            return
        
        print(f"\nCurrent demo user details:")
        print(f"Email: {demo_user.email}")
        print(f"Name: {demo_user.name}")
        print(f"Role: {demo_user.role}")
        print(f"Hashed Password: {demo_user.hashed_password[:50]}...")
        
        # Verify password
        password_correct = verify_password("Demo@123", demo_user.hashed_password)
        print(f"\nPassword 'Demo@123' is {'CORRECT' if password_correct else 'INCORRECT'}")
        
        if not password_correct:
            print("\nUpdating password to 'Demo@123'...")
            demo_user.hashed_password = get_password_hash("Demo@123")
            db.commit()
            print("✓ Password updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_demo_user()
