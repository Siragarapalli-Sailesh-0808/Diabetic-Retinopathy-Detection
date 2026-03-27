#!/bin/bash

# Deployment script for Render
echo "🚀 Starting deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p models_saved

# Check if models exist
if [ ! -f "models_saved/feature_extractor.h5" ] || [ ! -f "models_saved/vit_classifier.weights.h5" ]; then
    echo "🤖 Models not found. Training models..."
    echo "⚠️  This will take 10-15 minutes on first deployment..."
    python train_quick.py
else
    echo "✅ Models already exist"
fi

# Initialize database and create demo user
echo "🗄️  Initializing database..."
python create_demo_user.py

echo "✅ Deployment preparation complete!"
echo "🌐 Starting FastAPI server..."
