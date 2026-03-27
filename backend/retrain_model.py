"""
Quick Model Retraining Script
Retrains the model on the current dataset to improve accuracy
"""

import os
import sys
import numpy as np
from pathlib import Path
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Add paths
sys.path.append(os.path.dirname(__file__))

from training.dataset_loader import load_dataset
from training.feature_extractor import HybridCNNFeatureExtractor
from training.vit_classifier import VisionTransformerClassifier

def retrain_model():
    """Retrain the Vision Transformer classifier"""
    
    print("=" * 60)
    print("RETRAINING MODEL FOR BETTER ACCURACY")
    print("=" * 60)
    
    # Load dataset
    print("\n📂 Loading dataset...")
    dataset_dir = "./dataset"
    X_train, y_train, class_names = load_dataset(dataset_dir)
    print(f"✓ Loaded {len(X_train)} images")
    print(f"✓ Classes: {class_names}")
    
    # Split into train and validation
    X_train_split, X_val, y_train_split, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    print(f"✓ Train: {len(X_train_split)} images")
    print(f"✓ Validation: {len(X_val)} images")
    
    # Extract features
    print("\n🔧 Extracting features with CNN...")
    feature_extractor = HybridCNNFeatureExtractor()
    
    # Load existing feature extractor if available
    feature_extractor_path = "./models_saved/feature_extractor.h5"
    if os.path.exists(feature_extractor_path):
        feature_extractor.load(feature_extractor_path)
        print("✓ Loaded existing feature extractor")
    
    train_features = feature_extractor.extract_features(X_train_split)
    val_features = feature_extractor.extract_features(X_val)
    print(f"✓ Extracted features: {train_features.shape}")
    
    # Build and train ViT classifier
    print("\n🧠 Training Vision Transformer...")
    num_classes = len(class_names)
    feature_dim = train_features.shape[1]
    
    vit = VisionTransformerClassifier(
        feature_dim=feature_dim,
        num_classes=num_classes,
        num_transformer_blocks=6,  # Increased from 4
        num_heads=8,
        ff_dim=512,
        dropout_rate=0.2  # Increased dropout
    )
    
    # Compile
    vit.model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        )
    ]
    
    # Train
    print("\nTraining started...")
    history = vit.model.fit(
        train_features, y_train_split,
        validation_data=(val_features, y_val),
        epochs=100,
        batch_size=8,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    print("\n📊 Evaluating model...")
    train_loss, train_acc = vit.model.evaluate(train_features, y_train_split, verbose=0)
    val_loss, val_acc = vit.model.evaluate(val_features, y_val, verbose=0)
    
    print(f"\n✓ Training Accuracy: {train_acc*100:.2f}%")
    print(f"✓ Validation Accuracy: {val_acc*100:.2f}%")
    
    # Test predictions
    print("\n🔍 Testing predictions on validation set...")
    predictions = vit.predict(val_features)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Show confusion matrix
    from sklearn.metrics import classification_report, confusion_matrix
    print("\nClassification Report:")
    print(classification_report(y_val, predicted_classes, target_names=class_names))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_val, predicted_classes)
    print("Predicted →")
    print("Actual ↓")
    for i, class_name in enumerate(class_names):
        print(f"{class_name:15s}", end=" ")
        for j in range(num_classes):
            print(f"{cm[i][j]:3d}", end=" ")
        print()
    
    # Save model
    print("\n💾 Saving retrained model...")
    os.makedirs("./models_saved", exist_ok=True)
    vit_path = "./models_saved/vit_classifier.weights.h5"
    vit.save(vit_path)
    print(f"✓ Saved to {vit_path}")
    
    print("\n" + "=" * 60)
    print("✅ RETRAINING COMPLETE!")
    print("=" * 60)
    print("\n🔄 Restart the backend server to use the new model")
    print("   The predictions should now be more accurate!")
    
    return val_acc

if __name__ == "__main__":
    try:
        accuracy = retrain_model()
        print(f"\n🎯 Final Validation Accuracy: {accuracy*100:.2f}%")
    except Exception as e:
        print(f"\n❌ Error during retraining: {e}")
        import traceback
        traceback.print_exc()
