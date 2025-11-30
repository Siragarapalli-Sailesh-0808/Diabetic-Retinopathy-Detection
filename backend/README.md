# GAN-based Diabetic Retinopathy Detection System - Backend

FastAPI backend for DR detection with AI/ML pipeline.

## Quick Start

1. Create virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```powershell
   copy .env.example .env
   ```

4. Train the model (REQUIRED before first run):
   ```powershell
   python train.py
   ```

5. Run the server:
   ```powershell
   uvicorn app.main:app --reload
   ```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Endpoints

- `POST /auth/register` - Register user
- `POST /auth/login` - Login user
- `POST /api/upload` - Upload image
- `POST /api/predict` - Predict DR stage
- `GET /api/history` - Get prediction history
- `GET /api/metrics` - Get model metrics (admin/doctor only)

## Training

The `train.py` script performs:
1. Synthetic dataset generation
2. Image preprocessing
3. GAN training for augmentation
4. Feature extraction with hybrid CNNs
5. Vision Transformer training
6. Model evaluation and metrics saving

Training takes 10-20 minutes on a standard CPU.
