from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from ..base import PluginMetadata, ModelPlugin

class AnomalyDetectorPlugin(ModelPlugin):
    """A plugin that performs anomaly detection using Isolation Forest."""
    
    def __init__(self):
        self._config = {}
        self._model = None
        self._scaler = None
        self._feature_columns = None
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="anomaly_detector",
            version="1.0.0",
            description="Detects anomalies in data using Isolation Forest algorithm",
            author="ChatPlot",
            dependencies=["pandas", "numpy", "scikit-learn", "joblib"],
            entry_point="AnomalyDetectorPlugin",
            config_schema={
                "type": "object",
                "properties": {
                    "contamination": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 0.5
                    },
                    "n_estimators": {
                        "type": "integer",
                        "minimum": 50
                    },
                    "max_samples": {
                        "type": "string"
                    },
                    "random_state": {
                        "type": "integer"
                    },
                    "model_path": {
                        "type": "string"
                    }
                }
            }
        )
    
    def initialize(self, config: Optional[Dict] = None) -> None:
        """Initialize the plugin with configuration."""
        default_config = {
            "contamination": 0.1,
            "n_estimators": 100,
            "max_samples": "auto",
            "random_state": 42,
            "model_path": "models/anomaly_detector"
        }
        self._config = {**default_config, **(config or {})}
        
        # Create model directory if it doesn't exist
        os.makedirs(os.path.dirname(self._config["model_path"]), exist_ok=True)
        
        # Initialize model if saved model exists
        model_path = f"{self._config['model_path']}_model.joblib"
        scaler_path = f"{self._config['model_path']}_scaler.joblib"
        features_path = f"{self._config['model_path']}_features.joblib"
        
        if os.path.exists(model_path):
            self._model = joblib.load(model_path)
            self._scaler = joblib.load(scaler_path)
            self._feature_columns = joblib.load(features_path)
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass
    
    def train(self, data: Any, **kwargs) -> None:
        """Train the anomaly detection model."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        # Get feature columns
        self._feature_columns = kwargs.get("feature_columns")
        if not self._feature_columns:
            self._feature_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not self._feature_columns:
            raise ValueError("No numeric columns found for training")
        
        # Prepare training data
        X = data[self._feature_columns]
        
        # Initialize and fit scaler
        self._scaler = StandardScaler()
        X_scaled = self._scaler.fit_transform(X)
        
        # Initialize and train model
        self._model = IsolationForest(
            contamination=self._config["contamination"],
            n_estimators=self._config["n_estimators"],
            max_samples=self._config["max_samples"],
            random_state=self._config["random_state"]
        )
        
        self._model.fit(X_scaled)
        
        # Save model and scaler
        joblib.dump(self._model, f"{self._config['model_path']}_model.joblib")
        joblib.dump(self._scaler, f"{self._config['model_path']}_scaler.joblib")
        joblib.dump(self._feature_columns, f"{self._config['model_path']}_features.joblib")
    
    def predict(self, data: Any, **kwargs) -> Dict:
        """Detect anomalies in the input data."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        if self._model is None or self._scaler is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare input data
        if not all(col in data.columns for col in self._feature_columns):
            raise ValueError("Input data missing required features")
        
        X = data[self._feature_columns]
        X_scaled = self._scaler.transform(X)
        
        try:
            # Get anomaly scores and predictions
            scores = self._model.score_samples(X_scaled)
            predictions = self._model.predict(X_scaled)
            
            # Convert predictions from {-1, 1} to {True, False}
            anomalies = predictions == -1
            
            # Calculate threshold
            threshold = self._model.offset_
            
            # Prepare results
            results = {
                "anomalies": {
                    "indices": np.where(anomalies)[0].tolist(),
                    "scores": scores[anomalies].tolist(),
                    "data": data.iloc[anomalies].to_dict(orient="records")
                },
                "scores": {
                    "all": scores.tolist(),
                    "threshold": threshold,
                    "min": scores.min(),
                    "max": scores.max(),
                    "mean": scores.mean(),
                    "std": scores.std()
                },
                "summary": {
                    "total_samples": len(data),
                    "total_anomalies": anomalies.sum(),
                    "anomaly_rate": anomalies.mean(),
                    "feature_importance": self._calculate_feature_importance(X_scaled, scores)
                }
            }
            
            return results
            
        except Exception as e:
            return {
                "error": str(e),
                "anomalies": None,
                "scores": None,
                "summary": None
            }
    
    def _calculate_feature_importance(self, X: np.ndarray, scores: np.ndarray) -> Dict[str, float]:
        """Calculate feature importance based on correlation with anomaly scores."""
        importance = {}
        for i, feature in enumerate(self._feature_columns):
            correlation = np.corrcoef(X[:, i], scores)[0, 1]
            importance[feature] = abs(correlation)
        
        # Normalize importance scores
        total = sum(importance.values())
        if total > 0:
            importance = {k: v/total for k, v in importance.items()}
        
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True)) 