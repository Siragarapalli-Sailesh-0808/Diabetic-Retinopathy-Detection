from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # user, doctor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
