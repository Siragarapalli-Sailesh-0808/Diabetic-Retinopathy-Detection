# Windows Installation Guide

## Step-by-Step Installation for Windows

### 1. Verify Python Installation
```powershell
python --version
# Should show Python 3.8 or higher
```

### 2. Create and Activate Virtual Environment
```powershell
cd "C:\Users\NAGA PRASAD\Downloads\GAN-Driven_ Diabetic_Retinopathy_Detection\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Upgrade pip
```powershell
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install Dependencies in Steps

#### Step A: Install Core Web Framework
```powershell
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install python-multipart==0.0.6
```

#### Step B: Install Database
```powershell
pip install sqlalchemy==2.0.23
pip install aiosqlite==0.19.0
```

#### Step C: Install Validation
```powershell
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
```

#### Step D: Install Authentication
```powershell
pip install "python-jose[cryptography]==3.3.0"
pip install "passlib[bcrypt]==1.7.4"
pip install python-dotenv==1.0.0
```

#### Step E: Install Machine Learning (This may take 5-10 minutes)
```powershell
pip install numpy
pip install pillow
pip install opencv-python
pip install scikit-learn
pip install matplotlib
pip install tensorflow
```

**Note:** If TensorFlow installation fails, try:
```powershell
# For CPU-only version (recommended for Windows)
pip install tensorflow-cpu
```

### 5. Verify Installation
```powershell
python -c "import fastapi, uvicorn, sqlalchemy, numpy, tensorflow, cv2, sklearn; print('All packages installed successfully!')"
```

### 6. Create Environment File
```powershell
cp .env.example .env
```

Edit `.env` and set your secret:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./app.db
```

### 7. Initialize Database
```powershell
python setup_db.py
```

### 8. Train the Model (Optional - takes 15-30 minutes)
```powershell
python train.py
```

**Note:** You can skip training for now and test the API first. The prediction service will fail without trained models, but other endpoints will work.

### 9. Start the Backend Server
```powershell
uvicorn app.main:app --reload
```

Server will run on: http://localhost:8000
API docs available at: http://localhost:8000/docs

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'X'"
**Solution:** The package didn't install. Try:
```powershell
pip install X
```

### Error: Building wheel for TensorFlow failed
**Solution 1:** Install TensorFlow CPU version
```powershell
pip install tensorflow-cpu
```

**Solution 2:** Use pre-built wheels from unofficial sources (if above fails)
```powershell
# Visit: https://github.com/fo40225/tensorflow-windows-wheel
# Download appropriate .whl file for your Python version
pip install path\to\tensorflow-X.X.X-cpXX-cpXX-win_amd64.whl
```

### Error: "uvicorn: The term 'uvicorn' is not recognized"
**Solution:** Ensure virtual environment is activated and uvicorn is installed:
```powershell
.\venv\Scripts\Activate.ps1
pip install "uvicorn[standard]"
```

### Error: Execution Policy Error
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Cannot find path ... frontend"
**Solution:** Frontend is in a different folder. Use:
```powershell
cd ..
cd frontend
```

---

## Quick Test (Without Training)

If you want to test the API without waiting for model training:

1. Install all dependencies (Steps 1-6 above)
2. Run setup_db.py
3. Create a dummy models_saved directory:
```powershell
mkdir models_saved
```
4. Start the server:
```powershell
uvicorn app.main:app --reload
```

You can test:
- Health endpoint: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Register/Login endpoints

Prediction endpoint will fail until you run `python train.py` to create the models.

---

## Complete Installation Summary

```powershell
# 1. Setup
cd "C:\Users\NAGA PRASAD\Downloads\GAN-Driven_ Diabetic_Retinopathy_Detection\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel

# 2. Install packages
pip install fastapi==0.104.1 "uvicorn[standard]==0.24.0" python-multipart==0.0.6
pip install sqlalchemy==2.0.23 aiosqlite==0.19.0
pip install pydantic==2.5.0 pydantic-settings==2.1.0
pip install "python-jose[cryptography]==3.3.0" "passlib[bcrypt]==1.7.4" python-dotenv==1.0.0
pip install numpy pillow opencv-python scikit-learn matplotlib
pip install tensorflow-cpu

# 3. Setup environment
cp .env.example .env

# 4. Initialize database
python setup_db.py

# 5. (Optional) Train model
python train.py

# 6. Start server
uvicorn app.main:app --reload
```
