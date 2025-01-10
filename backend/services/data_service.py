import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import logging

class DataService:
    def __init__(self):
        self.current_data: Optional[pd.DataFrame] = None
        self.data_info: Dict = {}
        self.logger = logging.getLogger(__name__)

    def load_data(self, file_path: str, file_type: Optional[str] = None) -> Dict:
        """Load data from various file formats."""
        try:
            if file_type == 'csv' or file_path.endswith('.csv'):
                self.current_data = pd.read_csv(file_path)
            elif file_type == 'excel' or file_path.endswith(('.xls', '.xlsx')):
                self.current_data = pd.read_excel(file_path)
            elif file_type == 'json' or file_path.endswith('.json'):
                self.current_data = pd.read_json(file_path)
            elif file_path.endswith('.parquet'):
                self.current_data = pd.read_parquet(file_path)
            elif file_path.endswith('.feather'):
                self.current_data = pd.read_feather(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            self.data_info = self._analyze_data_structure()
            return self.data_info
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    def _analyze_data_structure(self) -> Dict:
        """Analyze the structure and properties of the loaded data."""
        if self.current_data is None:
            raise ValueError("No data loaded")

        info = {
            "shape": self.current_data.shape,
            "columns": self.current_data.columns.tolist(),
            "dtypes": self.current_data.dtypes.astype(str).to_dict(),
            "missing_values": self.current_data.isnull().sum().to_dict(),
            "numeric_columns": self.current_data.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": self.current_data.select_dtypes(include=['object', 'category']).columns.tolist(),
            "datetime_columns": self.current_data.select_dtypes(include=['datetime64']).columns.tolist(),
            "unique_counts": {col: self.current_data[col].nunique() for col in self.current_data.columns},
            "memory_usage": self.current_data.memory_usage(deep=True).sum()
        }

        # Add basic statistics for numeric columns
        if info["numeric_columns"]:
            info["numeric_summary"] = self.current_data[info["numeric_columns"]].describe().to_dict()

        # Add categorical summaries
        if info["categorical_columns"]:
            info["categorical_summary"] = {
                col: self.current_data[col].value_counts().head().to_dict()
                for col in info["categorical_columns"]
            }

        return info

    def process_data(self, operations: List[Dict]) -> pd.DataFrame:
        """Apply a series of data processing operations."""
        if self.current_data is None:
            raise ValueError("No data loaded")

        df = self.current_data.copy()

        for op in operations:
            try:
                op_type = op.get("type")
                if op_type == "filter":
                    df = self._apply_filter(df, op)
                elif op_type == "transform":
                    df = self._apply_transform(df, op)
                elif op_type == "aggregate":
                    df = self._apply_aggregation(df, op)
                elif op_type == "sort":
                    df = self._apply_sort(df, op)
                elif op_type == "clean":
                    df = self._apply_cleaning(df, op)
            except Exception as e:
                self.logger.error(f"Error processing operation {op_type}: {str(e)}")
                raise

        self.current_data = df
        return df

    def _apply_filter(self, df: pd.DataFrame, op: Dict) -> pd.DataFrame:
        """Apply filtering operations."""
        column = op.get("column")
        condition = op.get("condition")
        value = op.get("value")

        if condition == "equals":
            return df[df[column] == value]
        elif condition == "not_equals":
            return df[df[column] != value]
        elif condition == "greater_than":
            return df[df[column] > value]
        elif condition == "less_than":
            return df[df[column] < value]
        elif condition == "in":
            return df[df[column].isin(value)]
        elif condition == "not_in":
            return df[~df[column].isin(value)]
        elif condition == "contains":
            return df[df[column].str.contains(value, na=False)]
        elif condition == "between":
            return df[(df[column] >= value[0]) & (df[column] <= value[1])]
        else:
            raise ValueError(f"Unknown filter condition: {condition}")

    def _apply_transform(self, df: pd.DataFrame, op: Dict) -> pd.DataFrame:
        """Apply transformation operations."""
        transform_type = op.get("transform_type")
        columns = op.get("columns")

        if transform_type == "standardize":
            scaler = StandardScaler()
            df[columns] = scaler.fit_transform(df[columns])
        elif transform_type == "log":
            df[columns] = np.log1p(df[columns])
        elif transform_type == "one_hot":
            df = pd.get_dummies(df, columns=columns)
        elif transform_type == "bin":
            bins = op.get("bins", 10)
            for col in columns:
                df[f"{col}_binned"] = pd.qcut(df[col], bins, labels=False)
        elif transform_type == "pca":
            n_components = op.get("n_components", 2)
            pca = PCA(n_components=n_components)
            transformed = pca.fit_transform(df[columns])
            for i in range(n_components):
                df[f"PC{i+1}"] = transformed[:, i]
        else:
            raise ValueError(f"Unknown transform type: {transform_type}")

        return df

    def _apply_aggregation(self, df: pd.DataFrame, op: Dict) -> pd.DataFrame:
        """Apply aggregation operations."""
        group_by = op.get("group_by")
        agg_functions = op.get("functions", {})
        return df.groupby(group_by).agg(agg_functions).reset_index()

    def _apply_sort(self, df: pd.DataFrame, op: Dict) -> pd.DataFrame:
        """Apply sorting operations."""
        columns = op.get("columns")
        ascending = op.get("ascending", True)
        return df.sort_values(columns, ascending=ascending)

    def _apply_cleaning(self, df: pd.DataFrame, op: Dict) -> pd.DataFrame:
        """Apply data cleaning operations."""
        clean_type = op.get("clean_type")
        columns = op.get("columns")

        if clean_type == "drop_na":
            return df.dropna(subset=columns)
        elif clean_type == "fill_na":
            method = op.get("method", "mean")
            for col in columns:
                if method == "mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif method == "median":
                    df[col].fillna(df[col].median(), inplace=True)
                elif method == "mode":
                    df[col].fillna(df[col].mode()[0], inplace=True)
                elif method == "forward":
                    df[col].fillna(method="ffill", inplace=True)
                elif method == "backward":
                    df[col].fillna(method="bfill", inplace=True)
        elif clean_type == "remove_outliers":
            method = op.get("method", "zscore")
            threshold = op.get("threshold", 3)
            for col in columns:
                if method == "zscore":
                    z_scores = np.abs(stats.zscore(df[col]))
                    df = df[z_scores < threshold]
                elif method == "iqr":
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        elif clean_type == "drop_duplicates":
            df = df.drop_duplicates(subset=columns)

        return df

    def analyze_patterns(self, columns: Optional[List[str]] = None) -> Dict:
        """Analyze patterns in the data."""
        if self.current_data is None:
            raise ValueError("No data loaded")

        df = self.current_data[columns] if columns else self.current_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        patterns = {
            "correlation": self._analyze_correlation(df, numeric_cols),
            "trends": self._analyze_trends(df, numeric_cols),
            "clusters": self._analyze_clusters(df, numeric_cols),
            "seasonality": self._analyze_seasonality(df),
            "anomalies": self._detect_anomalies(df, numeric_cols)
        }

        return patterns

    def _analyze_correlation(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict:
        """Analyze correlations between numeric columns."""
        if len(numeric_cols) < 2:
            return {}

        corr_matrix = df[numeric_cols].corr()
        strong_correlations = []

        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.7:
                    strong_correlations.append({
                        "columns": (numeric_cols[i], numeric_cols[j]),
                        "correlation": corr
                    })

        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations
        }

    def _analyze_trends(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict:
        """Analyze trends in numeric columns."""
        trends = {}
        for col in numeric_cols:
            series = df[col].dropna()
            if len(series) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(series)), series)
                trends[col] = {
                    "slope": slope,
                    "r_squared": r_value ** 2,
                    "p_value": p_value,
                    "trend_direction": "increasing" if slope > 0 else "decreasing"
                }
        return trends

    def _analyze_clusters(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict:
        """Analyze clusters in numeric data."""
        if len(numeric_cols) < 2:
            return {}

        # Standardize the data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_cols])

        # Determine optimal number of clusters (up to 5)
        max_clusters = min(5, len(df) - 1)
        inertias = []
        for k in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_data)
            inertias.append(kmeans.inertia_)

        # Find elbow point
        optimal_clusters = 2  # default
        for i in range(1, len(inertias) - 1):
            if (inertias[i-1] - inertias[i]) / (inertias[i] - inertias[i+1]) < 0.5:
                optimal_clusters = i + 1
                break

        # Perform clustering with optimal number of clusters
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)

        return {
            "optimal_clusters": optimal_clusters,
            "cluster_sizes": np.bincount(clusters).tolist(),
            "cluster_centers": kmeans.cluster_centers_.tolist(),
            "inertia": kmeans.inertia_
        }

    def _analyze_seasonality(self, df: pd.DataFrame) -> Dict:
        """Analyze seasonality in time series data."""
        datetime_cols = df.select_dtypes(include=['datetime64']).columns
        seasonality = {}

        for col in datetime_cols:
            if len(df[col].dropna()) > 0:
                seasonality[col] = {
                    "daily": self._check_daily_pattern(df, col),
                    "weekly": self._check_weekly_pattern(df, col),
                    "monthly": self._check_monthly_pattern(df, col)
                }

        return seasonality

    def _detect_anomalies(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict:
        """Detect anomalies in numeric columns."""
        anomalies = {}
        for col in numeric_cols:
            series = df[col].dropna()
            if len(series) > 0:
                z_scores = np.abs(stats.zscore(series))
                anomalies[col] = {
                    "count": np.sum(z_scores > 3),
                    "indices": np.where(z_scores > 3)[0].tolist(),
                    "values": series[z_scores > 3].tolist()
                }
        return anomalies

    def _check_daily_pattern(self, df: pd.DataFrame, datetime_col: str) -> Dict:
        """Check for daily patterns in time series data."""
        df['hour'] = df[datetime_col].dt.hour
        hourly_stats = df.groupby('hour').agg(['mean', 'std']).to_dict()
        df.drop('hour', axis=1, inplace=True)
        return hourly_stats

    def _check_weekly_pattern(self, df: pd.DataFrame, datetime_col: str) -> Dict:
        """Check for weekly patterns in time series data."""
        df['dayofweek'] = df[datetime_col].dt.dayofweek
        daily_stats = df.groupby('dayofweek').agg(['mean', 'std']).to_dict()
        df.drop('dayofweek', axis=1, inplace=True)
        return daily_stats

    def _check_monthly_pattern(self, df: pd.DataFrame, datetime_col: str) -> Dict:
        """Check for monthly patterns in time series data."""
        df['month'] = df[datetime_col].dt.month
        monthly_stats = df.groupby('month').agg(['mean', 'std']).to_dict()
        df.drop('month', axis=1, inplace=True)
        return monthly_stats 