"""
Quick Training Script - Trains only on a subset for faster results
"""
import os
import sys
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import classification_report

sys.path.append(str(Path(__file__).parent))

from training.dataset_loader import RetinalDataset
from training.feature_extractor import HybridCNNFeatureExtractor
from training.vit_classifier import VisionTransformerClassifier

print("=" * 70)
print("Quick Training - Kaggle Retinal Dataset")
print("=" * 70)

# Use smaller subset for faster training
TRAIN_SIZE = 100  # Reduced from 150
VAL_SIZE = 20     # Reduced from 30
TEST_SIZE = 20    # Reduced from 30
BATCH_SIZE = 16
VIT_EPOCHS = 10   # Reduced from 20

# Load dataset
print("\nLoading dataset...")
dataset = RetinalDataset(data_dir="./data", image_size=(224, 224))
dataset.load_from_csv()

# Split dataset
train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = \
    dataset.split_dataset(train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)

# Use subset
train_paths = train_paths[:TRAIN_SIZE]
train_labels = train_labels[:TRAIN_SIZE]
val_paths = val_paths[:VAL_SIZE]
val_labels = val_labels[:VAL_SIZE]
test_paths = test_paths[:TEST_SIZE]
test_labels = test_labels[:TEST_SIZE]

print(f"\nUsing subset: Train={len(train_paths)}, Val={len(val_paths)}, Test={len(test_paths)}")

# Initialize feature extractor
print("\nLoading feature extractor...")
feature_extractor = HybridCNNFeatureExtractor()
feature_extractor.save("./models_saved/feature_extractor.h5")
print("Saved feature extractor")

# Extract features with progress
print("\nExtracting features...")

def extract_batch_features(paths, labels_list, batch_size=16):
    """Extract features in batches with progress"""
    all_features = []
    for i in range(0, len(paths), batch_size):
        batch_paths = paths[i:i+batch_size]
        images = dataset.load_images_to_memory(batch_paths)
        features = feature_extractor.extract_features(images)
        all_features.append(features)
        print(f"   {i+len(batch_paths)}/{len(paths)} images processed")
    
    return np.concatenate(all_features, axis=0), np.array(labels_list)

print("Train set...")
train_features, train_labels = extract_batch_features(train_paths, train_labels, BATCH_SIZE)

print("Val set...")
val_features, val_labels = extract_batch_features(val_paths, val_labels, BATCH_SIZE)

print("Test set...")
test_features, test_labels = extract_batch_features(test_paths, test_labels, BATCH_SIZE)

print(f"\nFeatures extracted: {train_features.shape}")

# Train ViT classifier
print("\nTraining Vision Transformer...")
vit_classifier = VisionTransformerClassifier(
    feature_dim=train_features.shape[1],
    num_classes=5,
    num_transformer_blocks=4,
    num_heads=8,
    ff_dim=256,
    dropout_rate=0.1
)

vit_classifier.model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7
    )
]

history = vit_classifier.model.fit(
    train_features, train_labels,
    validation_data=(val_features, val_labels),
    epochs=VIT_EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1
)

# Save model
vit_classifier.save("./models_saved/vit_classifier.weights.h5")
print("\nSaved ViT classifier")

# Evaluate
print("\nEvaluating...")
results = vit_classifier.model.evaluate(test_features, test_labels, verbose=1)
print(f"\nTest Loss: {results[0]:.4f}")
print(f"Test Accuracy: {results[1]:.4f}")

# Detailed metrics
predictions = vit_classifier.model.predict(test_features)
predicted_classes = np.argmax(predictions, axis=1)

class_names = ["No_DR", "Mild", "Moderate", "Severe", "Proliferative_DR"]
print("\nClassification Report:")
print(classification_report(test_labels, predicted_classes, target_names=class_names))

print("\nTraining Complete!")
print("Models saved in: ./models_saved/")
print("   - feature_extractor.h5")
print("   - vit_classifier.weights.h5")
