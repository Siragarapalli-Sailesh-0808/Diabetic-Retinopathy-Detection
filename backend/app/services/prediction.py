import os
import sys
import numpy as np
import requests
from typing import Tuple

# Add training module to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from training.preprocessing import preprocess_image

class PredictionService:
    """Service for making DR predictions"""
    UNCERTAIN_CLASS = -1
    
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

    UNCERTAIN_LABEL = "Uncertain - Retake Image"
    UNCERTAIN_EXPLANATION = (
        "The model is not confident enough for a reliable stage decision. "
        "Please upload a clearer, centered retinal fundus image or repeat capture."
    )
    
    def __init__(self, models_dir: str = "./models_saved"):
        self.models_dir = models_dir
        self.feature_extractor = None
        self.classifier = None
        self.feature_extractor_cls = None
        self.classifier_cls = None
        self.fallback_mode = False
        self._load_models()
    
    def _load_models(self):
        """Load the trained models"""
        try:
            feature_extractor_path = os.path.join(self.models_dir, "feature_extractor.h5")
            vit_path = os.path.join(self.models_dir, "vit_classifier.weights.h5")

            os.makedirs(self.models_dir, exist_ok=True)

            # Optional: fetch model artifacts from URLs for cloud hosts where large files are not in git.
            feature_url = os.getenv("MODEL_FEATURE_EXTRACTOR_URL", "").strip()
            vit_url = os.getenv("MODEL_VIT_WEIGHTS_URL", "").strip()
            if feature_url and not os.path.exists(feature_extractor_path):
                self._download_file(feature_url, feature_extractor_path)
            if vit_url and not os.path.exists(vit_path):
                self._download_file(vit_url, vit_path)

            if not os.path.exists(feature_extractor_path) or not os.path.exists(vit_path):
                self.fallback_mode = True
                print(
                    "Warning: Model files are missing. "
                    "Prediction service will use lightweight fallback mode."
                )
                return

            # Import TensorFlow-dependent modules only when real artifacts exist.
            from training.feature_extractor import HybridCNNFeatureExtractor
            from training.vit_classifier import VisionTransformerClassifier

            self.feature_extractor_cls = HybridCNNFeatureExtractor
            self.classifier_cls = VisionTransformerClassifier

            # Only build heavy TensorFlow models when artifacts are present.
            self.feature_extractor = self.feature_extractor_cls()
            self.feature_extractor.load(feature_extractor_path)
            print(f"Loaded feature extractor from {feature_extractor_path}")

            self.classifier = self.classifier_cls(num_classes=5, feature_dim=2560)
            self.classifier.load(vit_path)
            print(f"Loaded ViT classifier from {vit_path}")
        
        except Exception as e:
            print(f"Error loading models: {e}")
            raise

    def _download_file(self, url: str, destination: str):
        """Download a file from URL to destination path."""
        print(f"Downloading model artifact from: {url}")
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        print(f"Saved model artifact to: {destination}")
    
    def predict(self, image_path: str) -> Tuple[int, float, str, str]:
        """
        Make a prediction for a retinal image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Tuple of (predicted_class, confidence, class_name, explanation)
        """
        if self.feature_extractor is None or self.classifier is None:
            if not self.fallback_mode:
                raise RuntimeError("Models not loaded. Please check model files.")

        if self.fallback_mode:
            preprocessed = preprocess_image(image_path, target_size=(224, 224), validate=False)
            mean_intensity = float(np.mean(preprocessed))
            std_intensity = float(np.std(preprocessed))
            red_mean = float(np.mean(preprocessed[:, :, 0]))
            green_mean = float(np.mean(preprocessed[:, :, 1]))

            # Heuristic severity score based on darkness, contrast, and red/green balance.
            brightness_term = float(np.clip((0.55 - mean_intensity) / 0.35, 0.0, 1.0))
            contrast_term = float(np.clip((std_intensity - 0.12) / 0.22, 0.0, 1.0))
            rg_balance = red_mean - green_mean
            color_term = float(np.clip((rg_balance - 0.03) / 0.20, 0.0, 1.0))
            lesion_score = (0.50 * contrast_term) + (0.35 * brightness_term) + (0.15 * color_term)

            if lesion_score < 0.18:
                predicted_class = 0
            elif lesion_score < 0.36:
                predicted_class = 1
            elif lesion_score < 0.56:
                predicted_class = 2
            elif lesion_score < 0.76:
                predicted_class = 3
            else:
                predicted_class = 4

            confidence = float(0.52 + min(0.30, abs(lesion_score - 0.50) * 0.60))
            class_name = self.CLASS_NAMES[predicted_class]
            explanation = (
                self.EXPLANATIONS[predicted_class]
                + " (Fallback mode: full trained model artifacts are not available on server.)"
            )
            return predicted_class, confidence, class_name, explanation
        
        # Preprocess image
        preprocessed = preprocess_image(image_path, target_size=(224, 224))
        
        # Extract features (feature extractor handles batch dimension internally)
        features = self.feature_extractor.extract_features(preprocessed)
        
        # Get class probabilities and calibrate to reduce severe-class overprediction.
        probabilities = self.classifier.predict(features)
        calibrated = self._calibrate_probabilities(probabilities)
        probs = calibrated[0]
        
        # Log probabilities for debugging
        print(f"\n=== Prediction Probabilities ===")
        for i, prob in enumerate(probs):
            print(f"{self.CLASS_NAMES[i]}: {prob*100:.2f}%")
        print(f"================================\n")

        # Predict from calibrated probabilities.
        sorted_idx = np.argsort(probs)[::-1]
        predicted_class = int(sorted_idx[0])
        confidence = float(probs[sorted_idx[0]])
        second_best = float(probs[sorted_idx[1]])
        margin = confidence - second_best

        uncertainty_threshold = float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", "0.62"))
        margin_threshold = float(os.getenv("PREDICTION_MARGIN_THRESHOLD", "0.08"))
        if confidence < uncertainty_threshold or margin < margin_threshold:
            return (
                self.UNCERTAIN_CLASS,
                confidence,
                self.UNCERTAIN_LABEL,
                self.UNCERTAIN_EXPLANATION,
            )

        class_name = self.CLASS_NAMES[predicted_class]
        explanation = self.EXPLANATIONS[predicted_class]
        
        return predicted_class, confidence, class_name, explanation

    def _calibrate_probabilities(self, probabilities: np.ndarray) -> np.ndarray:
        """Apply lightweight class-wise calibration and renormalize probabilities."""
        # Slightly downweight severe classes; upweight early classes to reduce false severe calls.
        weights = np.array([1.06, 1.08, 1.00, 0.93, 0.87], dtype=np.float32)
        calibrated = probabilities * weights
        denom = np.sum(calibrated, axis=1, keepdims=True)
        denom = np.where(denom == 0, 1.0, denom)
        return calibrated / denom

# Global prediction service instance
prediction_service = None

def get_prediction_service() -> PredictionService:
    """Get or create prediction service instance"""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service
