import json
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def parse_data_request(message: str) -> Dict[str, Any]:
    """
    Parse a natural language data request into structured format
    """
    keywords = {
        'analysis': ['analyze', 'analyse', 'study', 'examine', 'investigate'],
        'visualization': ['plot', 'graph', 'chart', 'visualize', 'show'],
        'comparison': ['compare', 'contrast', 'versus', 'vs'],
        'trend': ['trend', 'over time', 'pattern', 'progression'],
        'distribution': ['distribute', 'spread', 'range', 'histogram'],
        'correlation': ['correlate', 'relationship', 'connection', 'between'],
    }

    request_type = None
    for key, words in keywords.items():
        if any(word in message.lower() for word in words):
            request_type = key
            break

    return {
        'type': request_type or 'analysis',
        'message': message
    }

def validate_data(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate data and return validation results
    """
    try:
        validation = {
            'is_valid': True,
            'issues': [],
            'warnings': []
        }

        # Check for empty dataframe
        if data.empty:
            validation['is_valid'] = False
            validation['issues'].append("Data is empty")
            return validation

        # Check for missing values
        missing_values = data.isnull().sum()
        if missing_values.any():
            validation['warnings'].append({
                'type': 'missing_values',
                'details': missing_values[missing_values > 0].to_dict()
            })

        # Check for constant columns
        constant_columns = [col for col in data.columns if data[col].nunique() == 1]
        if constant_columns:
            validation['warnings'].append({
                'type': 'constant_columns',
                'columns': constant_columns
            })

        # Check for high cardinality in categorical columns
        categorical_columns = data.select_dtypes(include=['object']).columns
        high_cardinality_threshold = len(data) * 0.5
        high_cardinality_columns = [
            col for col in categorical_columns
            if data[col].nunique() > high_cardinality_threshold
        ]
        if high_cardinality_columns:
            validation['warnings'].append({
                'type': 'high_cardinality',
                'columns': high_cardinality_columns
            })

        return validation

    except Exception as e:
        logger.error(f"Error in data validation: {str(e)}")
        return {
            'is_valid': False,
            'issues': [str(e)],
            'warnings': []
        }

def suggest_visualizations(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Suggest appropriate visualizations based on data characteristics
    """
    try:
        suggestions = []
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        categorical_columns = data.select_dtypes(exclude=[np.number]).columns

        # Time series check
        date_columns = [
            col for col in data.columns
            if pd.api.types.is_datetime64_any_dtype(data[col])
        ]

        if date_columns and len(numeric_columns) > 0:
            suggestions.append({
                'type': 'line',
                'description': 'Time series plot',
                'columns': {
                    'x': date_columns[0],
                    'y': numeric_columns[0]
                }
            })

        # Correlation heatmap for numeric data
        if len(numeric_columns) > 1:
            suggestions.append({
                'type': 'heatmap',
                'description': 'Correlation heatmap',
                'columns': list(numeric_columns)
            })

        # Bar charts for categorical data
        if len(categorical_columns) > 0 and len(numeric_columns) > 0:
            suggestions.append({
                'type': 'bar',
                'description': 'Bar chart',
                'columns': {
                    'x': categorical_columns[0],
                    'y': numeric_columns[0]
                }
            })

        # Scatter plot for numeric pairs
        if len(numeric_columns) > 1:
            suggestions.append({
                'type': 'scatter',
                'description': 'Scatter plot',
                'columns': {
                    'x': numeric_columns[0],
                    'y': numeric_columns[1]
                }
            })

        return suggestions

    except Exception as e:
        logger.error(f"Error suggesting visualizations: {str(e)}")
        return []

def format_insights(
    data: pd.DataFrame,
    analysis_type: str
) -> List[str]:
    """
    Generate insights based on data analysis
    """
    try:
        insights = []
        
        if analysis_type == "basic":
            # Basic statistics
            numeric_data = data.select_dtypes(include=[np.number])
            if not numeric_data.empty:
                for column in numeric_data.columns:
                    mean_val = data[column].mean()
                    std_val = data[column].std()
                    insights.append(
                        f"The average {column} is {mean_val:.2f} "
                        f"with a standard deviation of {std_val:.2f}"
                    )

        elif analysis_type == "correlation":
            # Correlation analysis
            numeric_data = data.select_dtypes(include=[np.number])
            if len(numeric_data.columns) > 1:
                corr_matrix = numeric_data.corr()
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                        corr = corr_matrix.iloc[i, j]
                        if abs(corr) > 0.5:
                            insights.append(
                                f"Strong {'positive' if corr > 0 else 'negative'} "
                                f"correlation ({corr:.2f}) between {col1} and {col2}"
                            )

        elif analysis_type == "distribution":
            # Distribution analysis
            numeric_data = data.select_dtypes(include=[np.number])
            for column in numeric_data.columns:
                skew = data[column].skew()
                if abs(skew) > 1:
                    insights.append(
                        f"{column} shows {'positive' if skew > 0 else 'negative'} "
                        f"skewness ({skew:.2f})"
                    )

        return insights

    except Exception as e:
        logger.error(f"Error formatting insights: {str(e)}")
        return [f"Error generating insights: {str(e)}"] 