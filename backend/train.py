"""
Training Script for Kaggle Retinal Disease Classification Dataset
Trains the Hybrid CNN Feature Extractor and Vision Transformer Classifier
on real retinal images
"""

import os
import sys
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from sklearn.utils.class_weight import compute_class_weight

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from training.dataset_loader import RetinalDataset
from training.feature_extractor import HybridCNNFeatureExtractor
from training.vit_classifier import VisionTransformerClassifier

class ModelTrainer:
    """Trains the DR detection model on Kaggle dataset"""
    
    def __init__(self, data_dir: str = "./data", models_dir: str = "./models_saved"):
        self.data_dir = data_dir
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        self.feature_extractor = None
        self.vit_classifier = None
        self.dataset = None
        
    def load_dataset(self):
        """Load and prepare the Kaggle dataset"""
        print("=" * 70)
        print("📊 Loading Kaggle Retinal Disease Classification Dataset")
        print("=" * 70)
        
        self.dataset = RetinalDataset(data_dir=self.data_dir, image_size=(224, 224))
        
        # Try loading from CSV first (most common format)
        try:
            self.dataset.load_from_csv()
        except Exception as e:
            print(f"⚠️  CSV loading failed: {e}")
            print("   Trying directory structure...")
            try:
                self.dataset.load_from_directory(split_by_folder=False)
            except Exception as e2:
                print(f"❌ Directory loading failed: {e2}")
                raise ValueError("Could not load dataset. Please check the data directory.")
        
        return self.dataset
    
    def prepare_data_splits(self, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """Split dataset into train/val/test"""
        print("\n" + "=" * 70)
        print("🔀 Splitting Dataset")
        print("=" * 70)
        
        splits = self.dataset.split_dataset(
            train_ratio=train_ratio,
            val_ratio=val_ratio,
            test_ratio=test_ratio
        )
        
        return splits
    
    def train_feature_extractor(self, train_paths, train_labels, val_paths, val_labels,
                                epochs=10, batch_size=32):
        """
        Train the Hybrid CNN Feature Extractor
        
        Note: The feature extractor uses pre-trained ImageNet weights,
        so we can optionally fine-tune it or use it as-is.
        """
        print("\n" + "=" * 70)
        print("🧠 Training Hybrid CNN Feature Extractor")
        print("=" * 70)
        
        # Initialize feature extractor
        self.feature_extractor = HybridCNNFeatureExtractor()
        
        # For this architecture, we use pre-trained ImageNet weights
        # No additional training needed unless you want to fine-tune
        print("✅ Using pre-trained ImageNet weights for feature extraction")
        
        # Save the feature extractor
        save_path = self.models_dir / "feature_extractor.h5"
        self.feature_extractor.save(str(save_path))
        print(f"💾 Saved feature extractor to {save_path}")
        
        return self.feature_extractor
    
    def extract_features(self, image_paths, labels, batch_size=32):
        """Extract features from images using the trained feature extractor"""
        print(f"\n🔍 Extracting features from {len(image_paths)} images...")
        
        # Load images in batches
        all_features = []
        all_labels = []
        
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i+batch_size]
            batch_labels = labels[i:i+batch_size]
            
            # Load and preprocess images
            images = self.dataset.load_images_to_memory(batch_paths)
            
            # Extract features
            features = self.feature_extractor.extract_features(images)
            all_features.append(features)
            all_labels.extend(batch_labels)
            
            if (i // batch_size + 1) % 5 == 0:
                print(f"   Processed {i + len(batch_paths)}/{len(image_paths)} images...")
        
        features = np.concatenate(all_features, axis=0)
        labels = np.array(all_labels)
        
        print(f"✅ Extracted features shape: {features.shape}")
        
        return features, labels
    
    def train_vit_classifier(self, train_features, train_labels, 
                            val_features, val_labels,
                            epochs=50, batch_size=32, learning_rate=0.0001):
        """Train the Vision Transformer Classifier"""
        print("\n" + "=" * 70)
        print("🤖 Training Vision Transformer Classifier")
        print("=" * 70)
        
        # Initialize ViT classifier
        self.vit_classifier = VisionTransformerClassifier(
            feature_dim=train_features.shape[1],  # 2560 for hybrid CNN
            num_classes=5,
            num_transformer_blocks=4,
            num_heads=8,
            ff_dim=256,
            dropout_rate=0.1
        )

        # Handle class imbalance in DR datasets (usually many class 0 and fewer class 3/4).
        unique_classes = np.unique(train_labels)
        weights = compute_class_weight(
            class_weight='balanced',
            classes=unique_classes,
            y=train_labels
        )
        class_weight = {int(cls): float(w) for cls, w in zip(unique_classes, weights)}
        print(f"   Class weights: {class_weight}")
        
        # Compile model
        self.vit_classifier.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(self.models_dir / 'vit_best_weights.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=True,
                verbose=1
            )
        ]
        
        # Train
        print(f"\n🚀 Training on {len(train_features)} samples...")
        print(f"   Validation: {len(val_features)} samples")
        print(f"   Epochs: {epochs}, Batch size: {batch_size}")
        
        history = self.vit_classifier.model.fit(
            train_features, train_labels,
            validation_data=(val_features, val_labels),
            epochs=epochs,
            batch_size=batch_size,
            class_weight=class_weight,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        save_path = self.models_dir / "vit_classifier.weights.h5"
        self.vit_classifier.save(str(save_path))
        print(f"\n💾 Saved ViT classifier to {save_path}")
        
        return history
    
    def evaluate(self, test_features, test_labels):
        """Evaluate the trained model"""
        print("\n" + "=" * 70)
        print("📊 Evaluating Model")
        print("=" * 70)
        
        # Evaluate
        results = self.vit_classifier.model.evaluate(test_features, test_labels, verbose=1)
        
        print(f"\n✅ Test Loss: {results[0]:.4f}")
        print(f"✅ Test Accuracy: {results[1]:.4f}")
        
        # Detailed predictions
        predictions = self.vit_classifier.predict(test_features)
        predicted_classes = np.argmax(predictions, axis=1)
        
        # Confusion matrix
        from sklearn.metrics import confusion_matrix, classification_report
        
        cm = confusion_matrix(test_labels, predicted_classes)
        print("\n📈 Confusion Matrix:")
        print(cm)
        
        print("\n📋 Classification Report:")
        class_names = ["No_DR", "Mild", "Moderate", "Severe", "Proliferative_DR"]
        print(classification_report(test_labels, predicted_classes, target_names=class_names))
        
        return results
    
    def save_training_log(self, history):
        """Save training history"""
        log_path = self.models_dir / f"training_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(log_path, 'w') as f:
            f.write("Training History\n")
            f.write("=" * 70 + "\n\n")
            
            for key in history.history.keys():
                f.write(f"{key}:\n")
                f.write(str(history.history[key]) + "\n\n")
        
        print(f"📝 Saved training log to {log_path}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 70)
    print("🚀 GAN-Based Diabetic Retinopathy Detection - Training Pipeline")
    print("   Using Kaggle Retinal Disease Classification Dataset")
    print("=" * 70 + "\n")
    
    # Configuration
    seed = int(os.getenv("TRAIN_SEED", "42"))
    np.random.seed(seed)
    tf.random.set_seed(seed)

    DATA_DIR = os.getenv("DATA_DIR", "./data")
    MODELS_DIR = os.getenv("MODELS_DIR", "./models_saved")
    DATA_CSV_PATH = os.getenv("DATA_CSV_PATH", "").strip() or None
    DATA_IMAGES_DIR = os.getenv("DATA_IMAGES_DIR", "").strip() or None
    
    BATCH_SIZE = 32
    VIT_EPOCHS = 50
    LEARNING_RATE = 0.0001
    
    # Initialize trainer
    trainer = ModelTrainer(data_dir=DATA_DIR, models_dir=MODELS_DIR)
    
    # Step 1: Load dataset
    if DATA_CSV_PATH is not None or DATA_IMAGES_DIR is not None:
        print("Using dataset paths from environment...")
        trainer.dataset = RetinalDataset(data_dir=DATA_DIR, image_size=(224, 224))
        trainer.dataset.load_from_csv(csv_path=DATA_CSV_PATH, images_dir=DATA_IMAGES_DIR)
    else:
        trainer.load_dataset()
    
    # Step 2: Split data
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = \
        trainer.prepare_data_splits(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
    
    # Step 3: Train/Load feature extractor
    trainer.train_feature_extractor(train_paths, train_labels, val_paths, val_labels)
    
    # Step 4: Extract features
    print("\n📦 Extracting features for training set...")
    train_features, train_labels = trainer.extract_features(train_paths, train_labels, batch_size=BATCH_SIZE)
    
    print("\n📦 Extracting features for validation set...")
    val_features, val_labels = trainer.extract_features(val_paths, val_labels, batch_size=BATCH_SIZE)
    
    print("\n📦 Extracting features for test set...")
    test_features, test_labels = trainer.extract_features(test_paths, test_labels, batch_size=BATCH_SIZE)
    
    # Step 5: Train ViT classifier
    history = trainer.train_vit_classifier(
        train_features, train_labels,
        val_features, val_labels,
        epochs=VIT_EPOCHS,
        batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE
    )
    
    # Step 6: Evaluate
    trainer.evaluate(test_features, test_labels)
    
    # Step 7: Save training log
    trainer.save_training_log(history)
    
    print("\n" + "=" * 70)
    print("🎉 Training Complete!")
    print("=" * 70)
    print(f"\n📁 Models saved in: {MODELS_DIR}/")
    print(f"   - feature_extractor.h5")
    print(f"   - vit_classifier.weights.h5")
    print(f"   - vit_best_weights.h5 (best validation accuracy)")
    print("\n✅ Models are ready for deployment!")


if __name__ == "__main__":
    main()
