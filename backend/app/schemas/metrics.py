from pydantic import BaseModel
from datetime import datetime
from typing import List

class MetricsBase(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: str

class MetricsCreate(MetricsBase):
    pass

class Metrics(MetricsBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    created_at: datetime
