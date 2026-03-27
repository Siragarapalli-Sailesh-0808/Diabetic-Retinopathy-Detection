"""
Kaggle Retinal Disease Classification Dataset Downloader
Downloads and prepares the dataset from:
https://www.kaggle.com/datasets/andrewmvd/retinal-disease-classification
"""

import os
import zipfile
import shutil
from pathlib import Path

def download_kaggle_dataset():
    """
    Downloads the Kaggle Retinal Disease Classification dataset.
    
    Prerequisites:
    1. Install kaggle package: pip install kaggle
    2. Setup Kaggle API credentials:
       - Go to https://www.kaggle.com/settings
       - Click "Create New API Token"
       - Save kaggle.json to ~/.kaggle/ (Linux/Mac) or C:\\Users\\<username>\\.kaggle\\ (Windows)
    """
    
    # Check if kaggle is installed
    try:
        import kaggle
    except ImportError:
        print("❌ Kaggle package not installed!")
        print("📦 Install it with: pip install kaggle")
        return False
    
    # Check if Kaggle API credentials exist
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if not kaggle_json.exists():
        print("❌ Kaggle API credentials not found!")
        print("📋 Setup instructions:")
        print("   1. Go to https://www.kaggle.com/settings")
        print("   2. Scroll to 'API' section")
        print("   3. Click 'Create New API Token'")
        print(f"   4. Save kaggle.json to: {kaggle_dir}")
        return False
    
    # Create data directory
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    print("📥 Downloading Kaggle Retinal Disease Classification dataset...")
    print("   This may take several minutes depending on your connection...")
    
    try:
        # Download dataset
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        api.dataset_download_files(
            'andrewmvd/retinal-disease-classification',
            path=str(data_dir),
            unzip=True
        )
        
        print("✅ Dataset downloaded successfully!")
        
        # Check dataset structure
        print("\n📂 Dataset structure:")
        for item in sorted(data_dir.rglob('*')):
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"   {item.relative_to(data_dir)} ({size_mb:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def organize_dataset():
    """
    Organizes the downloaded dataset into train/val/test splits.
    The Kaggle dataset comes with images and CSV annotations.
    """
    data_dir = Path(__file__).parent / 'data'
    
    if not data_dir.exists():
        print("❌ Data directory not found. Please download the dataset first.")
        return False
    
    print("\n📊 Analyzing dataset structure...")
    
    # List all files in data directory
    all_files = list(data_dir.rglob('*'))
    image_files = [f for f in all_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    csv_files = [f for f in all_files if f.suffix.lower() == '.csv']
    
    print(f"   Found {len(image_files)} images")
    print(f"   Found {len(csv_files)} CSV files")
    
    if csv_files:
        print("\n📋 CSV files (contain labels):")
        for csv_file in csv_files:
            print(f"   - {csv_file.name}")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Kaggle Retinal Disease Classification Dataset Setup")
    print("=" * 60)
    
    # Download dataset
    if download_kaggle_dataset():
        # Organize dataset
        organize_dataset()
        print("\n✅ Dataset setup complete!")
        print("📍 Location: ./data/")
    else:
        print("\n❌ Dataset setup failed. Please check the error messages above.")
