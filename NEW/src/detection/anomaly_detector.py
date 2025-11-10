"""
Anomaly Detection Module
Uses ML algorithms to detect network anomalies
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from pyod.models.auto_encoder import AutoEncoder
import pickle
import os


class AnomalyDetector:
    def __init__(self, model_type='isolation_forest', contamination=0.1):
        self.model_type = model_type
        self.contamination = contamination
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the selected ML model"""
        if self.model_type == 'isolation_forest':
            self.model = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
        elif self.model_type == 'ocsvm':
            self.model = OneClassSVM(
                nu=self.contamination,
                kernel='rbf',
                gamma='auto'
            )
        elif self.model_type == 'lof':
            self.model = LocalOutlierFactor(
                contamination=self.contamination,
                novelty=True
            )
        elif self.model_type == 'autoencoder':
            self.model = AutoEncoder(
                contamination=self.contamination,
                hidden_neurons=[64, 32, 32, 64]
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def preprocess_data(self, df):
        """Extract features from packet data"""
        if df.empty:
            return pd.DataFrame()
        
        features = pd.DataFrame()
        
        # Numeric features
        features['length'] = df['length']
        features['src_port'] = df['src_port'].fillna(0)
        features['dst_port'] = df['dst_port'].fillna(0)
        
        # Protocol encoding
        protocol_map = {'TCP': 0, 'UDP': 1, 'ICMP': 2, 'OTHER': 3}
        features['protocol'] = df['protocol'].map(protocol_map).fillna(3)
        
        # Time-based features
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            features['hour'] = df['timestamp'].dt.hour
            features['minute'] = df['timestamp'].dt.minute
            features['second'] = df['timestamp'].dt.second
        
        # IP-based features (simplified)
        if 'src_ip' in df.columns:
            features['src_ip_last_octet'] = df['src_ip'].apply(
                lambda x: int(str(x).split('.')[-1]) if pd.notna(x) else 0
            )
        if 'dst_ip' in df.columns:
            features['dst_ip_last_octet'] = df['dst_ip'].apply(
                lambda x: int(str(x).split('.')[-1]) if pd.notna(x) else 0
            )
        
        return features.fillna(0)
    
    def train(self, df):
        """Train the anomaly detection model"""
        features = self.preprocess_data(df)
        
        if features.empty or len(features) < 10:
            print("Insufficient data for training")
            return False
        
        # Scale features
        X_scaled = self.scaler.fit_transform(features)
        
        # Train model
        try:
            self.model.fit(X_scaled)
            self.is_trained = True
            print(f"Model trained on {len(features)} samples")
            return True
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict(self, df):
        """Predict anomalies in new data"""
        if not self.is_trained:
            return np.array([])
        
        features = self.preprocess_data(df)
        
        if features.empty:
            return np.array([])
        
        try:
            X_scaled = self.scaler.transform(features)
            predictions = self.model.predict(X_scaled)
            
            # Convert to binary (1 = anomaly, 0 = normal)
            # Isolation Forest: -1 = anomaly, 1 = normal
            if self.model_type in ['isolation_forest', 'ocsvm', 'lof']:
                predictions = np.where(predictions == -1, 1, 0)
            
            return predictions
        except Exception as e:
            print(f"Prediction error: {e}")
            return np.array([0] * len(features))
    
    def get_anomaly_scores(self, df):
        """Get anomaly scores for each sample"""
        if not self.is_trained:
            return np.array([])
        
        features = self.preprocess_data(df)
        
        if features.empty:
            return np.array([])
        
        try:
            X_scaled = self.scaler.transform(features)
            
            if hasattr(self.model, 'decision_function'):
                scores = self.model.decision_function(X_scaled)
                # Normalize scores to 0-1 range
                scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
            elif hasattr(self.model, 'score_samples'):
                scores = -self.model.score_samples(X_scaled)
                scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
            else:
                scores = np.zeros(len(features))
            
            return scores
        except Exception as e:
            print(f"Scoring error: {e}")
            return np.array([0.0] * len(features))
    
    def save_model(self, filepath):
        """Save trained model to disk"""
        if not self.is_trained:
            print("No trained model to save")
            return False
        
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'scaler': self.scaler,
                    'model_type': self.model_type,
                    'contamination': self.contamination
                }, f)
            print(f"Model saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath):
        """Load trained model from disk"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.model_type = data['model_type']
                self.contamination = data['contamination']
                self.is_trained = True
            print(f"Model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
