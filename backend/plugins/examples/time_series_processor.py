from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from scipy import stats
from ..base import PluginMetadata, DataProcessorPlugin

class TimeSeriesProcessorPlugin(DataProcessorPlugin):
    """A plugin that provides advanced time series processing capabilities."""
    
    def __init__(self):
        self._config = {}
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="time_series_processor",
            version="1.0.0",
            description="Provides advanced time series analysis and processing capabilities",
            author="ChatPlot",
            dependencies=["pandas", "numpy", "statsmodels", "scipy"],
            entry_point="TimeSeriesProcessorPlugin",
            config_schema={
                "type": "object",
                "properties": {
                    "decomposition_model": {
                        "type": "string",
                        "enum": ["additive", "multiplicative"]
                    },
                    "seasonal_period": {"type": "integer"},
                    "outlier_threshold": {"type": "number"}
                }
            }
        )
    
    def initialize(self, config: Optional[Dict] = None) -> None:
        """Initialize the plugin with configuration."""
        default_config = {
            "decomposition_model": "additive",
            "seasonal_period": 12,
            "outlier_threshold": 3
        }
        self._config = {**default_config, **(config or {})}
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass
    
    def process_data(self, data: Any, **kwargs) -> Dict:
        """Process time series data and return analysis results."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        # Extract required columns
        date_col = kwargs.get("date_column")
        value_col = kwargs.get("value_column")
        
        if not date_col or not value_col:
            raise ValueError("Date and value columns must be specified")
        
        if date_col not in data.columns or value_col not in data.columns:
            raise ValueError("Specified columns not found in DataFrame")
        
        # Ensure datetime index
        df = data.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df.set_index(date_col, inplace=True)
        
        # Sort index
        df.sort_index(inplace=True)
        
        results = {
            "original_data": df[value_col].to_dict(),
            "decomposition": self._decompose_series(df[value_col]),
            "stationarity": self._check_stationarity(df[value_col]),
            "outliers": self._detect_outliers(df[value_col]),
            "summary_stats": self._calculate_summary_stats(df[value_col])
        }
        
        return results
    
    def _decompose_series(self, series: pd.Series) -> Dict:
        """Decompose time series into trend, seasonal, and residual components."""
        try:
            # Perform decomposition
            decomposition = seasonal_decompose(
                series,
                model=self._config["decomposition_model"],
                period=self._config["seasonal_period"]
            )
            
            return {
                "trend": decomposition.trend.fillna(method="bfill").fillna(method="ffill").to_dict(),
                "seasonal": decomposition.seasonal.fillna(method="bfill").fillna(method="ffill").to_dict(),
                "residual": decomposition.resid.fillna(method="bfill").fillna(method="ffill").to_dict()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "trend": None,
                "seasonal": None,
                "residual": None
            }
    
    def _check_stationarity(self, series: pd.Series) -> Dict:
        """Check time series stationarity using Augmented Dickey-Fuller test."""
        try:
            # Perform ADF test
            adf_result = adfuller(series.dropna())
            
            return {
                "is_stationary": adf_result[1] < 0.05,
                "adf_statistic": adf_result[0],
                "p_value": adf_result[1],
                "critical_values": adf_result[4]
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "is_stationary": None,
                "adf_statistic": None,
                "p_value": None,
                "critical_values": None
            }
    
    def _detect_outliers(self, series: pd.Series) -> Dict:
        """Detect outliers using z-score method."""
        try:
            # Calculate z-scores
            z_scores = np.abs(stats.zscore(series.dropna()))
            threshold = self._config["outlier_threshold"]
            outlier_indices = np.where(z_scores > threshold)[0]
            
            return {
                "outlier_indices": outlier_indices.tolist(),
                "outlier_values": series.iloc[outlier_indices].to_dict(),
                "total_outliers": len(outlier_indices)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "outlier_indices": None,
                "outlier_values": None,
                "total_outliers": None
            }
    
    def _calculate_summary_stats(self, series: pd.Series) -> Dict:
        """Calculate summary statistics for the time series."""
        try:
            return {
                "mean": series.mean(),
                "std": series.std(),
                "min": series.min(),
                "max": series.max(),
                "median": series.median(),
                "skewness": series.skew(),
                "kurtosis": series.kurtosis(),
                "first_value": series.iloc[0],
                "last_value": series.iloc[-1],
                "total_change": series.iloc[-1] - series.iloc[0],
                "percent_change": ((series.iloc[-1] - series.iloc[0]) / series.iloc[0]) * 100
            }
            
        except Exception as e:
            return {
                "error": str(e)
            } 