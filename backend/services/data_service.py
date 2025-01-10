import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
import logging
import json
from pathlib import Path
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from config import settings

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self, data_dir: str = settings.UPLOAD_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.current_data: Optional[pd.DataFrame] = None
        self.scaler = StandardScaler()
        self.cached_analyses: Dict[str, Any] = {}

    def load_data(
        self,
        file_path: Union[str, Path],
        file_type: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from various file formats with enhanced error handling and type inference
        """
        try:
            file_path = Path(file_path)
            if file_type is None:
                file_type = file_path.suffix.lower()

            # Default options for data loading
            load_options = {
                'parse_dates': True,
                'infer_datetime_format': True,
                'low_memory': False,
                **kwargs
            }

            if file_type in ['.csv', '.txt']:
                data = pd.read_csv(file_path, **load_options)
            elif file_type in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path, **load_options)
            elif file_type == '.json':
                data = pd.read_json(file_path, **load_options)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            # Automatic data cleaning and type inference
            data = self._clean_and_infer_types(data)
            self.current_data = data
            return data

        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def process_data(
        self,
        data: pd.DataFrame,
        operations: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Process data with enhanced operations and error handling
        """
        try:
            processed_data = data.copy()

            for operation in operations:
                op_type = operation.get("type")
                params = operation.get("params", {})

                if op_type == "filter":
                    processed_data = self._apply_filter(processed_data, params)
                elif op_type == "sort":
                    processed_data = processed_data.sort_values(**params)
                elif op_type == "group":
                    processed_data = self._apply_grouping(processed_data, params)
                elif op_type == "transform":
                    processed_data = self._apply_transform(processed_data, params)
                elif op_type == "aggregate":
                    processed_data = self._apply_aggregation(processed_data, params)
                elif op_type == "clean":
                    processed_data = self._apply_cleaning(processed_data, params)
                else:
                    raise ValueError(f"Unsupported operation type: {op_type}")

            return processed_data

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise

    def get_data_summary(
        self,
        data: Optional[pd.DataFrame] = None,
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Generate comprehensive data summary with statistical analysis
        """
        try:
            if data is None:
                data = self.current_data
            if data is None:
                raise ValueError("No data available")

            numeric_columns = data.select_dtypes(include=[np.number]).columns
            categorical_columns = data.select_dtypes(exclude=[np.number]).columns
            datetime_columns = data.select_dtypes(include=['datetime64']).columns

            summary = {
                "shape": data.shape,
                "columns": list(data.columns),
                "numeric_columns": list(numeric_columns),
                "categorical_columns": list(categorical_columns),
                "datetime_columns": list(datetime_columns),
                "missing_values": data.isnull().sum().to_dict(),
                "numeric_summary": data[numeric_columns].describe().to_dict() if len(numeric_columns) > 0 else {},
                "categorical_summary": {
                    col: data[col].value_counts().to_dict()
                    for col in categorical_columns
                }
            }

            if detailed:
                summary.update({
                    "correlations": self._calculate_correlations(data),
                    "outliers": self._detect_outliers(data),
                    "distributions": self._analyze_distributions(data),
                    "trends": self._analyze_trends(data),
                    "data_quality": self._assess_data_quality(data)
                })

            return summary

        except Exception as e:
            logger.error(f"Error generating data summary: {str(e)}")
            raise

    def _clean_and_infer_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean data and infer correct data types
        """
        # Remove completely empty columns and rows
        data = data.dropna(how='all', axis=1).dropna(how='all', axis=0)

        for column in data.columns:
            # Try to convert to numeric
            try:
                data[column] = pd.to_numeric(data[column])
                continue
            except (ValueError, TypeError):
                pass

            # Try to convert to datetime
            try:
                data[column] = pd.to_datetime(data[column])
                continue
            except (ValueError, TypeError):
                pass

            # Clean string columns
            if data[column].dtype == object:
                data[column] = data[column].astype(str).str.strip()

        return data

    def _apply_filter(
        self,
        data: pd.DataFrame,
        params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Apply advanced filtering with multiple conditions
        """
        if "query" in params:
            return data.query(params["query"])
        elif "conditions" in params:
            mask = pd.Series(True, index=data.index)
            for condition in params["conditions"]:
                column = condition["column"]
                operator = condition["operator"]
                value = condition["value"]

                if operator == "equals":
                    mask &= data[column] == value
                elif operator == "contains":
                    mask &= data[column].str.contains(value, na=False)
                elif operator == "greater_than":
                    mask &= data[column] > value
                elif operator == "less_than":
                    mask &= data[column] < value
                elif operator == "between":
                    mask &= (data[column] >= value[0]) & (data[column] <= value[1])

            return data[mask]
        return data

    def _apply_grouping(
        self,
        data: pd.DataFrame,
        params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Apply advanced grouping with multiple aggregations
        """
        grouped = data.groupby(**params)
        if "aggs" in params:
            return grouped.agg(params["aggs"])
        return grouped.agg(params.get("agg", "mean"))

    def _apply_transform(
        self,
        data: pd.DataFrame,
        params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Apply data transformations
        """
        if params.get("type") == "normalize":
            columns = params.get("columns", data.select_dtypes(include=[np.number]).columns)
            data[columns] = self.scaler.fit_transform(data[columns])
        elif params.get("type") == "pca":
            columns = params.get("columns", data.select_dtypes(include=[np.number]).columns)
            n_components = params.get("n_components", 2)
            pca = PCA(n_components=n_components)
            transformed = pca.fit_transform(data[columns])
            for i in range(n_components):
                data[f"PC{i+1}"] = transformed[:, i]
        return data

    def _calculate_correlations(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate various correlation metrics
        """
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return {}

        return {
            "pearson": numeric_data.corr(method='pearson').to_dict(),
            "spearman": numeric_data.corr(method='spearman').to_dict(),
            "kendall": numeric_data.corr(method='kendall').to_dict()
        }

    def _detect_outliers(
        self,
        data: pd.DataFrame,
        threshold: float = 1.5
    ) -> Dict[str, List[int]]:
        """
        Detect outliers using IQR method
        """
        outliers = {}
        numeric_columns = data.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            Q1 = data[column].quantile(0.25)
            Q3 = data[column].quantile(0.75)
            IQR = Q3 - Q1
            outlier_mask = (
                (data[column] < (Q1 - threshold * IQR)) |
                (data[column] > (Q3 + threshold * IQR))
            )
            if outlier_mask.any():
                outliers[column] = list(data.index[outlier_mask])

        return outliers

    def _analyze_distributions(self, data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Analyze distributions of numeric columns
        """
        distributions = {}
        numeric_columns = data.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            if data[column].nunique() > 1:
                distributions[column] = {
                    "skewness": float(stats.skew(data[column].dropna())),
                    "kurtosis": float(stats.kurtosis(data[column].dropna())),
                    "normality_test": float(stats.normaltest(data[column].dropna())[1])
                }

        return distributions

    def _analyze_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in time series data
        """
        trends = {}
        datetime_columns = data.select_dtypes(include=['datetime64']).columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns

        if not datetime_columns.empty and not numeric_columns.empty:
            date_col = datetime_columns[0]
            for num_col in numeric_columns:
                # Simple linear regression
                x = np.arange(len(data))
                y = data[num_col].values
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                
                trends[num_col] = {
                    "slope": float(slope),
                    "r_squared": float(r_value ** 2),
                    "p_value": float(p_value)
                }

        return trends

    def _assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess overall data quality
        """
        total_cells = data.shape[0] * data.shape[1]
        missing_cells = data.isnull().sum().sum()
        
        return {
            "completeness": 1 - (missing_cells / total_cells),
            "duplicates": len(data[data.duplicated()]),
            "zero_variance_columns": list(data.columns[data.std() == 0]),
            "high_cardinality_columns": [
                col for col in data.select_dtypes(include=['object']).columns
                if data[col].nunique() / len(data) > 0.5
            ]
        }

    def save_data(
        self,
        data: pd.DataFrame,
        file_name: str,
        file_type: str = "csv"
    ) -> str:
        """
        Save data to a file
        """
        try:
            file_path = self.data_dir / f"{file_name}.{file_type}"
            
            if file_type == "csv":
                data.to_csv(file_path, index=False)
            elif file_type == "excel":
                data.to_excel(file_path, index=False)
            elif file_type == "json":
                data.to_json(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            return str(file_path)

        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise

    def get_correlation_matrix(
        self,
        data: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Calculate correlation matrix for numeric columns
        """
        try:
            if data is None:
                data = self.current_data
            if data is None:
                raise ValueError("No data available")

            numeric_data = data.select_dtypes(include=[np.number])
            return numeric_data.corr()

        except Exception as e:
            logger.error(f"Error calculating correlation matrix: {str(e)}")
            raise 