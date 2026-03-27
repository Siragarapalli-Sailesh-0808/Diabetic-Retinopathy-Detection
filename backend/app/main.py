from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .database import init_db, SessionLocal
from .models.user import User
from .services.auth import get_password_hash
from .routes import auth, predictions

# Initialize FastAPI app
app = FastAPI(
    title="GAN-based Diabetic Retinopathy Detection System",
    description="AI-powered system for detecting and classifying diabetic retinopathy stages",
    version="1.0.0"
)

# Configure CORS
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]  # React/Vite dev servers on localhost or 127.0.0.1

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    # Allow Vercel preview and production domains without redeploying backend for each preview URL.
    allow_origin_regex=r"https://.*\.vercel\.app",
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

    # Ensure demo credentials are always available for local testing.
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@demo.com").first()
        if demo_user is None:
            db.add(
                User(
                    email="demo@demo.com",
                    name="Demo User",
                    hashed_password=get_password_hash("Demo@123"),
                    role="patient"
                )
            )
            db.commit()
            print("Demo user created: demo@demo.com")
    except Exception as e:
        db.rollback()
        print(f"Warning: Could not ensure demo user: {e}")
    finally:
        db.close()
    
    # On constrained hosts (e.g., free tiers), preload can crash cold starts.
    preload_models = os.getenv("LOAD_MODELS_ON_STARTUP", "false").lower() == "true"
    if preload_models:
        try:
            from .services.prediction import get_prediction_service
            get_prediction_service()
            print("Prediction service loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load prediction service: {e}")
            print("Please run train.py to train the model first")
    else:
        print("Skipping model preload on startup (LOAD_MODELS_ON_STARTUP=false)")

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
