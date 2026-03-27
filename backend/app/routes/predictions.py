from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime
import json

from ..database import get_db
from ..models.user import User
from ..models.prediction import Prediction
from ..models.metrics import ModelMetrics
from ..schemas.prediction import PredictionResponse, Prediction as PredictionSchema
from ..schemas.metrics import MetricsResponse
from ..services.auth import get_current_user, get_current_admin_or_doctor
from ..services.prediction import get_prediction_service

router = APIRouter(prefix="/api", tags=["Predictions"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def validate_image_file(filename: str) -> bool:
    """Validate if file is an allowed image type"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a retinal image"""
    
    # Validate file type
    if not validate_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create user-specific directory
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(user_dir, filename)
    
    # Save file
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    
    return {
        "message": "File uploaded successfully",
        "filename": filename,
        "filepath": filepath
    }

@router.post("/predict", response_model=PredictionResponse)
async def predict_dr(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict diabetic retinopathy stage from uploaded image"""
    
    # Validate file type
    if not validate_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create user-specific directory
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(user_dir, filename)
    
    # Save file
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    
    # Make prediction
    try:
        pred_service = get_prediction_service()
        predicted_class, confidence, class_name, explanation = pred_service.predict(filepath)
    except ValueError as e:
        # Validation error - image is not a retinal image
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Clean up file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
    
    # Save prediction to database
    prediction = Prediction(
        user_id=current_user.id,
        image_path=filepath,
        predicted_class=predicted_class,
        confidence=confidence
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return {
        "predicted_class": predicted_class,
        "class_name": class_name,
        "confidence": confidence,
        "explanation": explanation,
        "image_path": filepath
    }

@router.get("/history", response_model=List[PredictionSchema])
async def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prediction history for current user"""
    
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).all()
    
    return predictions

@router.get("/metrics", response_model=MetricsResponse)
async def get_model_metrics(
    current_user: User = Depends(get_current_admin_or_doctor),
    db: Session = Depends(get_db)
):
    """Get model performance metrics (admin/doctor only)"""
    
    # Get latest metrics
    metrics = db.query(ModelMetrics).order_by(
        ModelMetrics.created_at.desc()
    ).first()
    
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metrics found. Please run training first."
        )
    
    # Parse confusion matrix
    confusion_matrix = json.loads(metrics.confusion_matrix)
    
    return {
        "accuracy": metrics.accuracy,
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1_score": metrics.f1_score,
        "confusion_matrix": confusion_matrix,
        "created_at": metrics.created_at
    }
