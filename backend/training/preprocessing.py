"""Preprocessing utilities for retinal images"""
import cv2
import numpy as np

def is_retinal_image(image_path: str) -> tuple[bool, str]:
    """
    Check if an image appears to be a retinal fundus image.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return False, "Could not read image file"
    
    # Convert to RGB and HSV for analysis
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check 1: Image should be reasonably sized
    height, width = img.shape[:2]
    if height < 100 or width < 100:
        return False, "Image is too small. Please upload a high-quality retinal image (minimum 100x100 pixels)"
    
    # Check 2: Retinal images typically have circular or oval regions (dark background)
    # Calculate the ratio of dark pixels (background should be dark in retinal images)
    dark_pixels = np.sum(img_gray < 50)
    total_pixels = img_gray.size
    dark_ratio = dark_pixels / total_pixels
    
    # Retinal images usually have 15-50% dark background
    if dark_ratio < 0.05:
        return False, "This doesn't appear to be a retinal image. Retinal images should have a dark background with a circular illuminated region showing the back of the eye"
    
    # Check 3: Color distribution - retinal images have reddish/orange tones
    mean_color = np.mean(img_rgb, axis=(0, 1))
    # Red channel should be dominant in retinal images
    if mean_color[0] < mean_color[2]:  # Red should be greater than Blue
        return False, "Color distribution suggests this is not a retinal image. Retinal images typically have warm red/orange tones from blood vessels"
    
    # Check 4: Detect circular/oval regions (retinal images have circular field of view)
    # Apply edge detection
    edges = cv2.Canny(img_gray, 50, 150)
    
    # Use Hough Circle detection
    circles = cv2.HoughCircles(
        img_gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=height//2,
        param1=50, 
        param2=30, 
        minRadius=height//6, 
        maxRadius=height//2
    )
    
    # If no circular region detected, might not be a retinal image
    if circles is None or len(circles[0]) == 0:
        return False, "No circular retinal region detected. Please upload a proper retinal fundus photograph showing the circular field of view"
    
    return True, ""

def preprocess_image(image_path: str, target_size: tuple = (224, 224), validate: bool = True) -> np.ndarray:
    """
    Preprocess retinal image for model input.
    
    Args:
        image_path: Path to the image file
        target_size: Target size for the image (height, width)
        validate: Whether to validate if image is a retinal image
    
    Returns:
        Preprocessed image array
    
    Raises:
        ValueError: If image validation fails
    """
    # Validate if it's a retinal image
    if validate:
        is_valid, error_msg = is_retinal_image(image_path)
        if not is_valid:
            raise ValueError(f"Invalid retinal image: {error_msg}")
    
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
