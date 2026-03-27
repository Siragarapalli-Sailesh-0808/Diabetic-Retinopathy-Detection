import os
import sys
import numpy as np
from tensorflow import keras
from typing import Tuple
import json

# Add training module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from training.preprocessing import preprocess_image
from training.feature_extractor import HybridCNNFeatureExtractor, preprocess_for_cnn
from training.vit_classifier import VisionTransformerClassifier, MultiHeadSelfAttention, TransformerBlock

class PredictionService:
    """Service for making DR predictions"""
    
    # Class names and descriptions
    CLASS_NAMES = {
        0: "No DR",
        1: "Mild DR",
        2: "Moderate DR",
        3: "Severe DR",
        4: "Proliferative DR"
    }
    
    EXPLANATIONS = {
        0: "No signs of diabetic retinopathy detected. Continue regular monitoring and maintain good blood sugar control.",
        1: "Mild diabetic retinopathy detected with microaneurysms. Regular follow-up recommended. Maintain strict blood glucose control.",
        2: "Moderate diabetic retinopathy with visible hemorrhages and microaneurysms. Close monitoring required. Consult with an ophthalmologist.",
        3: "Severe diabetic retinopathy with extensive hemorrhages and cotton-wool spots. Urgent ophthalmologist consultation recommended.",
        4: "Proliferative diabetic retinopathy with neovascularization. Immediate treatment required. High risk of vision loss without intervention."
    }
    
    def __init__(self, models_dir: str = "./models_saved"):
        self.models_dir = models_dir
        self.feature_extractor = None
        self.classifier = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained models"""
        try:
            # Load feature extractor
            feature_extractor_path = os.path.join(self.models_dir, "feature_extractor.h5")
            if os.path.exists(feature_extractor_path):
                self.feature_extractor = HybridCNNFeatureExtractor()
                self.feature_extractor.load(feature_extractor_path)
                print(f"Loaded feature extractor from {feature_extractor_path}")
            else:
                print(f"Warning: Feature extractor not found at {feature_extractor_path}")
                print("Creating new feature extractor (will use pre-trained CNN weights)")
                self.feature_extractor = HybridCNNFeatureExtractor()
            
            # Load ViT classifier
            vit_path = os.path.join(self.models_dir, "vit_classifier.weights.h5")
            if os.path.exists(vit_path):
                # Create new model instance and load weights
                self.classifier = VisionTransformerClassifier(num_classes=5, feature_dim=2560)
                self.classifier.load(vit_path)
                print(f"Loaded ViT classifier from {vit_path}")
            else:
                raise FileNotFoundError(
                    f"ViT classifier not found at {vit_path}. "
                    "Please run train.py first to train the model."
                )
        
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def predict(self, image_path: str) -> Tuple[int, float, str, str]:
        """
        Make a prediction for a retinal image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Tuple of (predicted_class, confidence, class_name, explanation)
        """
        if self.feature_extractor is None or self.classifier is None:
            raise RuntimeError("Models not loaded. Please check model files.")
        
        # Preprocess image
        preprocessed = preprocess_image(image_path, target_size=(224, 224))
        
        # Extract features (feature extractor handles batch dimension internally)
        features = self.feature_extractor.extract_features(preprocessed)
        
        # Get all class probabilities for debugging
        probabilities = self.classifier.predict(features)
        
        # Log probabilities for debugging
        print(f"\n=== Prediction Probabilities ===")
        for i, prob in enumerate(probabilities[0]):
            print(f"{self.CLASS_NAMES[i]}: {prob*100:.2f}%")
        print(f"================================\n")
        
        # Predict
        predicted_class, confidence = self.classifier.predict_class(features)
        
        predicted_class = int(predicted_class[0])
        confidence = float(confidence[0])
        class_name = self.CLASS_NAMES[predicted_class]
        explanation = self.EXPLANATIONS[predicted_class]
        
        return predicted_class, confidence, class_name, explanation

# Global prediction service instance
prediction_service = None

def get_prediction_service() -> PredictionService:
    """Get or create prediction service instance"""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service
