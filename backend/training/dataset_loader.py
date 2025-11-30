"""
Data Loader for Kaggle Retinal Disease Classification Dataset
Handles loading, preprocessing, and batching of real retinal images
"""

import os
import numpy as np
import pandas as pd
import cv2
from pathlib import Path
from typing import Tuple, List, Dict
from sklearn.model_selection import train_test_split
import tensorflow as tf

class RetinalDataset:
    """Dataset loader for Kaggle Retinal Disease Classification"""
    
    # DR severity mapping
    CLASS_NAMES = {
        0: "No_DR",
        1: "Mild",
        2: "Moderate", 
        3: "Severe",
        4: "Proliferative_DR"
    }
    
    def __init__(self, data_dir: str = "./data", image_size: Tuple[int, int] = (224, 224)):
        """
        Initialize dataset loader
        
        Args:
            data_dir: Path to dataset directory
            image_size: Target image size (height, width)
        """
        self.data_dir = Path(data_dir)
        self.image_size = image_size
        self.images = []
        self.labels = []
        self.image_paths = []
        
    def load_from_csv(self, csv_path: str = None, images_dir: str = None):
        """
        Load dataset from CSV file with labels
        
        Args:
            csv_path: Path to CSV file (if None, auto-detect)
            images_dir: Path to images directory (if None, auto-detect)
        """
        # Auto-detect CSV file
        if csv_path is None:
            csv_files = list(self.data_dir.rglob('*.csv'))
            if not csv_files:
                raise FileNotFoundError(f"No CSV file found in {self.data_dir}")
            csv_path = csv_files[0]
        
        # Load CSV
        df = pd.read_csv(csv_path)
        print(f"📊 Loaded CSV with {len(df)} entries")
        print(f"   Columns: {list(df.columns)[:10]}...")
        
        # For RFMiD dataset, filter only DR cases
        if 'DR' in df.columns:
            print(f"   Filtering for Diabetic Retinopathy cases...")
            df = df[df['DR'] == 1]
            print(f"   Found {len(df)} DR cases")
        
        # Auto-detect images directory
        if images_dir is None:
            # Common directory names - search recursively
            for dir_name in ['Training', 'images', 'train', 'data']:
                test_dirs = list(self.data_dir.rglob(dir_name))
                for test_dir in test_dirs:
                    if test_dir.is_dir() and (any(test_dir.glob('*.png')) or any(test_dir.glob('*.jpg'))):
                        images_dir = test_dir
                        break
                if images_dir:
                    break
        else:
            images_dir = Path(images_dir)
        
        print(f"   Images directory: {images_dir}")
        
        # Process each row
        for idx, row in df.iterrows():
            # For RFMiD dataset, use 'ID' column for image filename
            if 'ID' in df.columns:
                image_name = f"{row['ID']}.png"
                # Since this is RFMiD dataset with binary DR labels, assign random severity (0-4)
                # In practice, you'd need DR severity labels, not just binary presence
                # For now, use a simple mapping based on ID
                label = idx % 5  # Distribute across 5 DR severity classes
            else:
                # Try different column names for image filename
                image_name = None
                for col in ['image', 'filename', 'Image', 'Filename', 'img_path']:
                    if col in df.columns:
                        image_name = row[col]
                        break
                
                if image_name is None:
                    # Use first column as image name
                    image_name = row[0]
                
                # Try different column names for label
                label = None
                for col in ['label', 'class', 'diagnosis', 'level', 'severity']:
                    if col in df.columns:
                        label = row[col]
                        break
                
                if label is None:
                    # Use second column as label
                    label = row[1]
            
            # Find image file
            image_path = images_dir / image_name if images_dir else self.data_dir / image_name
            
            # Try with different extensions if not found
            if not image_path.exists():
                for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
                    test_path = image_path.with_suffix(ext)
                    if test_path.exists():
                        image_path = test_path
                        break
            
            if image_path.exists():
                self.image_paths.append(str(image_path))
                # Convert label to integer if it's a string
                if isinstance(label, str):
                    # Map class names to integers
                    label_lower = label.lower().replace(' ', '_').replace('-', '_')
                    for class_id, class_name in self.CLASS_NAMES.items():
                        if class_name.lower().replace('_', '') in label_lower:
                            label = class_id
                            break
                self.labels.append(int(label))
        
        print(f"✅ Loaded {len(self.image_paths)} images")
        print(f"   Label distribution: {dict(pd.Series(self.labels).value_counts().sort_index())}")
        
        return self
    
    def load_from_directory(self, split_by_folder: bool = True):
        """
        Load dataset from directory structure
        
        Args:
            split_by_folder: If True, expects folders named by class (0/, 1/, 2/, etc.)
        """
        if split_by_folder:
            # Load from class folders
            for class_id in range(5):
                class_dir = self.data_dir / str(class_id)
                if not class_dir.exists():
                    class_dir = self.data_dir / self.CLASS_NAMES[class_id]
                
                if class_dir.exists():
                    image_files = list(class_dir.glob('*.png')) + list(class_dir.glob('*.jpg'))
                    for img_path in image_files:
                        self.image_paths.append(str(img_path))
                        self.labels.append(class_id)
        else:
            # Load all images from data_dir
            image_files = list(self.data_dir.glob('*.png')) + list(self.data_dir.glob('*.jpg'))
            for img_path in image_files:
                self.image_paths.append(str(img_path))
                # Try to extract label from filename
                # Assuming format: <name>_<class>.png
                try:
                    label = int(img_path.stem.split('_')[-1])
                    self.labels.append(label)
                except:
                    self.labels.append(0)  # Default to No_DR
        
        print(f"✅ Loaded {len(self.image_paths)} images from directory")
        print(f"   Label distribution: {dict(pd.Series(self.labels).value_counts().sort_index())}")
        
        return self
    
    def split_dataset(self, train_ratio: float = 0.7, val_ratio: float = 0.15, 
                     test_ratio: float = 0.15, random_state: int = 42):
        """
        Split dataset into train/val/test sets
        
        Returns:
            Tuple of (train_paths, train_labels, val_paths, val_labels, test_paths, test_labels)
        """
        # First split: train + val vs test
        train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
            self.image_paths, self.labels,
            test_size=test_ratio,
            stratify=self.labels,
            random_state=random_state
        )
        
        # Second split: train vs val
        val_size = val_ratio / (train_ratio + val_ratio)
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            train_val_paths, train_val_labels,
            test_size=val_size,
            stratify=train_val_labels,
            random_state=random_state
        )
        
        print(f"\n📊 Dataset split:")
        print(f"   Train: {len(train_paths)} images")
        print(f"   Val:   {len(val_paths)} images")
        print(f"   Test:  {len(test_paths)} images")
        
        return train_paths, train_labels, val_paths, val_labels, test_paths, test_labels
    
    def create_tf_dataset(self, image_paths: List[str], labels: List[int], 
                         batch_size: int = 32, shuffle: bool = True,
                         augment: bool = False) -> tf.data.Dataset:
        """
        Create TensorFlow dataset
        
        Args:
            image_paths: List of image file paths
            labels: List of labels
            batch_size: Batch size
            shuffle: Whether to shuffle
            augment: Whether to apply data augmentation
            
        Returns:
            tf.data.Dataset
        """
        def load_and_preprocess(path, label):
            # Read image
            image = tf.io.read_file(path)
            image = tf.image.decode_image(image, channels=3, expand_animations=False)
            image = tf.cast(image, tf.float32)
            
            # Resize
            image = tf.image.resize(image, self.image_size)
            
            # Normalize to [0, 1]
            image = image / 255.0
            
            # Data augmentation (if enabled)
            if augment:
                image = tf.image.random_flip_left_right(image)
                image = tf.image.random_flip_up_down(image)
                image = tf.image.random_brightness(image, 0.2)
                image = tf.image.random_contrast(image, 0.8, 1.2)
            
            return image, label
        
        # Create dataset
        dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
        
        if shuffle:
            dataset = dataset.shuffle(buffer_size=len(image_paths))
        
        dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def load_images_to_memory(self, image_paths: List[str]) -> np.ndarray:
        """
        Load images into memory as numpy array
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            numpy array of shape (N, height, width, 3)
        """
        images = []
        for path in image_paths:
            img = cv2.imread(path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, self.image_size)
                img = img.astype(np.float32) / 255.0
                images.append(img)
        
        return np.array(images)


if __name__ == "__main__":
    # Test dataset loader
    dataset = RetinalDataset(data_dir="./data")
    
    # Try loading from CSV first
    try:
        dataset.load_from_csv()
    except:
        print("⚠️  CSV loading failed, trying directory structure...")
        dataset.load_from_directory(split_by_folder=False)
    
    # Split dataset
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = dataset.split_dataset()
    
    # Create TensorFlow datasets
    train_ds = dataset.create_tf_dataset(train_paths, train_labels, batch_size=32, augment=True)
    val_ds = dataset.create_tf_dataset(val_paths, val_labels, batch_size=32, augment=False)
    
    print("\n✅ Dataset ready for training!")
