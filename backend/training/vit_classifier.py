"""Vision Transformer classifier"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Tuple

class MultiHeadSelfAttention(layers.Layer):
    """Multi-head self-attention layer"""
    
    def __init__(self, embed_dim, num_heads=8, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.projection_dim = embed_dim // num_heads
        self.query_dense = layers.Dense(embed_dim)
        self.key_dense = layers.Dense(embed_dim)
        self.value_dense = layers.Dense(embed_dim)
        self.combine_heads = layers.Dense(embed_dim)

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        query = self.query_dense(inputs)
        key = self.key_dense(inputs)
        value = self.value_dense(inputs)
        
        query = tf.reshape(query, (batch_size, -1, self.num_heads, self.projection_dim))
        query = tf.transpose(query, perm=[0, 2, 1, 3])
        key = tf.reshape(key, (batch_size, -1, self.num_heads, self.projection_dim))
        key = tf.transpose(key, perm=[0, 2, 1, 3])
        value = tf.reshape(value, (batch_size, -1, self.num_heads, self.projection_dim))
        value = tf.transpose(value, perm=[0, 2, 1, 3])
        
        score = tf.matmul(query, key, transpose_b=True)
        dim_key = tf.cast(tf.shape(key)[-1], tf.float32)
        scaled_score = score / tf.math.sqrt(dim_key)
        weights = tf.nn.softmax(scaled_score, axis=-1)
        attention = tf.matmul(weights, value)
        
        attention = tf.transpose(attention, perm=[0, 2, 1, 3])
        concat_attention = tf.reshape(attention, (batch_size, -1, self.embed_dim))
        output = self.combine_heads(concat_attention)
        return output

    def get_config(self):
        config = super().get_config()
        config.update({"embed_dim": self.embed_dim, "num_heads": self.num_heads})
        return config
    
    @classmethod
    def from_config(cls, config):
        return cls(**config)

class TransformerBlock(layers.Layer):
    """Transformer block"""
    
    def __init__(self, embed_dim, num_heads, ff_dim, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.att = MultiHeadSelfAttention(embed_dim, num_heads)
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation="relu"),
            layers.Dense(embed_dim),
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "dropout_rate": self.dropout_rate,
        })
        return config
    
    @classmethod
    def from_config(cls, config):
        return cls(**config)

class VisionTransformerClassifier:
    """Vision Transformer classifier"""
    
    def __init__(self, feature_dim=2560, num_classes=5, num_transformer_blocks=4, 
                 num_heads=8, ff_dim=512, dropout_rate=0.1):
        self.feature_dim = feature_dim
        self.num_classes = num_classes
        self.num_transformer_blocks = num_transformer_blocks
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        self.model = self._build_model()
    
    def _build_model(self):
        """Build the model"""
        inputs = layers.Input(shape=(self.feature_dim,))
        x = layers.Reshape((1, self.feature_dim))(inputs)
        
        positions = tf.range(start=0, limit=1, delta=1)
        position_embedding = layers.Embedding(input_dim=1, output_dim=self.feature_dim)(positions)
        x = x + position_embedding
        
        for _ in range(self.num_transformer_blocks):
            x = TransformerBlock(self.feature_dim, self.num_heads, self.ff_dim, self.dropout_rate)(x)
        
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(256, activation="relu")(x)
        x = layers.Dropout(self.dropout_rate)(x)
        x = layers.Dense(128, activation="relu")(x)
        x = layers.Dropout(self.dropout_rate)(x)
        outputs = layers.Dense(self.num_classes, activation="softmax")(x)
        
        return keras.Model(inputs=inputs, outputs=outputs)
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict class probabilities"""
        return self.model.predict(features, verbose=0)
    
    def predict_class(self, features: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict DR class and confidence.
        
        Args:
            features: Input features
        
        Returns:
            Tuple of (predicted_classes, confidences)
        """
        probabilities = self.predict(features)
        predicted_classes = np.argmax(probabilities, axis=1)
        confidences = np.max(probabilities, axis=1)
        return predicted_classes, confidences
    
    def save(self, filepath: str):
        """Save model weights"""
        self.model.save_weights(filepath)
    
    def load(self, filepath: str):
        """Load model weights"""
        self.model.load_weights(filepath)
