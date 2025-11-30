from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .database import init_db
from .routes import auth, predictions

# Initialize FastAPI app
app = FastAPI(
    title="GAN-based Diabetic Retinopathy Detection System",
    description="AI-powered system for detecting and classifying diabetic retinopathy stages",
    version="1.0.0"
)

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://siragarapalli-sailesh-0808.github.io",
]
# Combine default and environment-specified origins
all_origins = list(set(DEFAULT_ORIGINS + [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(predictions.router)

# Mount uploads directory for serving images (optional)
uploads_dir = os.getenv("UPLOAD_DIR", "./uploads")
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")
    
    # Try to load prediction service
    try:
        from .services.prediction import get_prediction_service
        get_prediction_service()
        print("Prediction service loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load prediction service: {e}")
        print("Please run train.py to train the model first")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GAN-based Diabetic Retinopathy Detection System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
