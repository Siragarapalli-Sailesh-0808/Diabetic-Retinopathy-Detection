"""Feature extraction using hybrid CNN"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import VGG16, MobileNet, DenseNet121
import numpy as np

def preprocess_for_cnn(image: np.ndarray) -> np.ndarray:
    """Preprocess image for CNN"""
    return np.expand_dims(image, axis=0)

class HybridCNNFeatureExtractor:
    """Hybrid CNN using VGG16, MobileNet, and DenseNet121"""
    
    def __init__(self):
        self.model = None
        self._build_model()
    
    def _build_model(self):
        """Build the hybrid CNN model"""
        input_layer = keras.layers.Input(shape=(224, 224, 3))
        
        # VGG16
        vgg16 = VGG16(weights='imagenet', include_top=False, pooling='avg')
        vgg16_features = vgg16(input_layer)
        
        # MobileNet
        mobilenet = MobileNet(weights='imagenet', include_top=False, pooling='avg')
        mobilenet_features = mobilenet(input_layer)
        
        # DenseNet121
        densenet = DenseNet121(weights='imagenet', include_top=False, pooling='avg')
        densenet_features = densenet(input_layer)
        
        # Concatenate features
        concatenated = keras.layers.Concatenate()([
            vgg16_features,
            mobilenet_features,
            densenet_features
        ])
        
        self.model = keras.Model(inputs=input_layer, outputs=concatenated)
    
    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """Extract features from image"""
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        return self.model.predict(image, verbose=0)
    
    def save(self, filepath: str):
        """Save the model"""
        self.model.save(filepath)
    
    def load(self, filepath: str):
        """Load the model"""
        self.model = keras.models.load_model(filepath, compile=False)
