"""Preprocessing utilities for retinal images"""
import cv2
import numpy as np

def preprocess_image(image_path: str, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess retinal image for model input.
    
    Args:
        image_path: Path to the image file
        target_size: Target size for the image (height, width)
    
    Returns:
        Preprocessed image array
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")
    
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize
    img = cv2.resize(img, target_size)
    
    # Normalize to [0, 1]
    img = img.astype(np.float32) / 255.0
    
    return img

def preprocess_for_cnn(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for CNN feature extraction.
    
    Args:
        image: Preprocessed image array
    
    Returns:
        Image array ready for CNN input
    """
    # Add batch dimension
    return np.expand_dims(image, axis=0)
