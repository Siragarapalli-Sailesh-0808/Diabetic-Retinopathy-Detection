from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from ..database import Base

class ModelMetrics(Base):
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    confusion_matrix = Column(String, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
