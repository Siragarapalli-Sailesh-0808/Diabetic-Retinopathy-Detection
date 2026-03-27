from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PredictionBase(BaseModel):
    image_path: str
    predicted_class: int
    confidence: float

class PredictionCreate(PredictionBase):
    user_id: int

class Prediction(PredictionBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    predicted_class: int
    class_name: str
    confidence: float
    explanation: str
    image_path: str
