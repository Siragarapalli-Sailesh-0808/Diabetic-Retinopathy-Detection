#!/bin/bash
# Build script for Render

echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p uploads models_saved data

echo "Build complete!"
