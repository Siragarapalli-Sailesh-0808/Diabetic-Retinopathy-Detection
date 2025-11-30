# GAN-Driven Diabetic Retinopathy Detection System

An AI-powered web application for detecting and classifying diabetic retinopathy stages using GAN-based deep learning models.

## Features

- 🔬 **AI-Powered Detection**: Uses Vision Transformer (ViT) and MobileNet for accurate DR classification
- 🎨 **GAN-Based Augmentation**: Synthetic data generation for improved model training
- 🔐 **User Authentication**: Secure login/registration system
- 📊 **Dashboard**: Interactive interface for image upload and analysis
- 🏥 **Multi-Stage Classification**: Detects No DR, Mild, Moderate, Severe, and Proliferative DR
- 📈 **Performance Metrics**: Real-time model performance tracking

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- TensorFlow/Keras (Deep Learning)
- SQLAlchemy (Database ORM)
- SQLite (Database)
- JWT Authentication

**Frontend:**
- React.js
- Axios (HTTP client)
- React Router

**ML Models:**
- Vision Transformer (ViT) Classifier
- MobileNet Feature Extractor
- GAN for data augmentation

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

5. Train the model (required before first run):
```bash
python train.py
```

6. Start the backend server:
```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## Quick Start (Windows)

Run the automated startup script:
```powershell
.\START_PROJECT.ps1
```

This will start both backend and frontend servers automatically.

## Usage

1. **Register/Login**: Create an account or login with demo credentials
   - Email: `demo@demo.com`
   - Password: `Demo@123`

2. **Upload Image**: Upload a retinal fundus image for analysis

3. **View Results**: Get instant DR classification and confidence scores

4. **Track History**: View past predictions in your dashboard

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Main Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /api/upload` - Upload retinal image
- `POST /api/predict` - Predict DR stage
- `GET /api/history` - Get prediction history
- `GET /api/metrics` - Get model metrics

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── routes/      # API routes
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── training/        # ML model training
│   ├── models_saved/    # Trained models
│   └── requirements.txt
├── frontend/
│   ├── public/
│   └── src/
│       ├── pages/       # React pages
│       ├── services/    # API services
│       └── styles/      # CSS files
└── README.md
```

## Model Information

- **Feature Extractor**: MobileNet pre-trained on ImageNet
- **Classifier**: Vision Transformer (ViT) architecture
- **Training Data**: RFMiD dataset with GAN augmentation
- **Classification Classes**: 5 (No DR, Mild, Moderate, Severe, Proliferative)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is created for educational and research purposes.

## Acknowledgments

- RFMiD Dataset for training data
- TensorFlow and Keras communities
- FastAPI and React communities

## Contact

For questions or support, please open an issue in the repository.
