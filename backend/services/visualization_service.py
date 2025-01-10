import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
import io
import base64
import logging

class VisualizationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.theme = "plotly_white"
        self.color_palette = px.colors.qualitative.Set3
        plt.style.use('seaborn')
        sns.set_theme(style="whitegrid")

    def create_visualization(
        self,
        data: pd.DataFrame,
        viz_type: str,
        x: Optional[str] = None,
        y: Optional[Union[str, List[str]]] = None,
        **kwargs
    ) -> Dict:
        """Create a visualization based on the specified type and parameters."""
        try:
            if viz_type == "line":
                fig = self._create_line_plot(data, x, y, **kwargs)
            elif viz_type == "bar":
                fig = self._create_bar_plot(data, x, y, **kwargs)
            elif viz_type == "scatter":
                fig = self._create_scatter_plot(data, x, y, **kwargs)
            elif viz_type == "histogram":
                fig = self._create_histogram(data, x, **kwargs)
            elif viz_type == "box":
                fig = self._create_box_plot(data, x, y, **kwargs)
            elif viz_type == "violin":
                fig = self._create_violin_plot(data, x, y, **kwargs)
            elif viz_type == "heatmap":
                fig = self._create_heatmap(data, **kwargs)
            elif viz_type == "pie":
                fig = self._create_pie_chart(data, **kwargs)
            elif viz_type == "area":
                fig = self._create_area_plot(data, x, y, **kwargs)
            elif viz_type == "parallel":
                fig = self._create_parallel_coordinates(data, **kwargs)
            elif viz_type == "scatter_matrix":
                fig = self._create_scatter_matrix(data, **kwargs)
            elif viz_type == "sunburst":
                fig = self._create_sunburst(data, **kwargs)
            elif viz_type == "distribution":
                fig = self._create_distribution_plot(data, x, **kwargs)
            elif viz_type == "bubble":
                fig = self._create_bubble_plot(data, **kwargs)
            elif viz_type == "radar":
                fig = self._create_radar_plot(data, **kwargs)
            elif viz_type == "treemap":
                fig = self._create_treemap(data, **kwargs)
            elif viz_type == "funnel":
                fig = self._create_funnel_plot(data, **kwargs)
            else:
                raise ValueError(f"Unsupported visualization type: {viz_type}")

            # Apply common styling
            self._apply_styling(fig, **kwargs)

            return {
                "plot": self._convert_to_json(fig),
                "type": viz_type,
                "parameters": {
                    "x": x,
                    "y": y,
                    **kwargs
                }
            }

        except Exception as e:
            self.logger.error(f"Error creating visualization: {str(e)}")
            raise

    def _create_line_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        **kwargs
    ) -> go.Figure:
        """Create an enhanced line plot with multiple series support."""
        if isinstance(y, str):
            fig = px.line(data, x=x, y=y, **kwargs)
        else:
            fig = go.Figure()
            for y_col in y:
                fig.add_trace(
                    go.Scatter(
                        x=data[x],
                        y=data[y_col],
                        name=y_col,
                        mode='lines+markers'
                    )
                )

        # Add trend lines if requested
        if kwargs.get("show_trend", False):
            for y_col in (y if isinstance(y, list) else [y]):
                self._add_trend_line(fig, data[x], data[y_col], y_col)

        return fig

    def _create_bar_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        **kwargs
    ) -> go.Figure:
        """Create an enhanced bar plot with multiple modes."""
        orientation = kwargs.get("orientation", "v")
        barmode = kwargs.get("barmode", "group")

        if isinstance(y, str):
            fig = px.bar(
                data,
                x=x,
                y=y,
                orientation=orientation,
                barmode=barmode,
                **kwargs
            )
        else:
            fig = go.Figure()
            for y_col in y:
                fig.add_trace(
                    go.Bar(
                        x=data[x] if orientation == "v" else data[y_col],
                        y=data[y_col] if orientation == "v" else data[x],
                        name=y_col,
                        orientation=orientation
                    )
                )

        # Add error bars if specified
        if "error_y" in kwargs:
            for trace in fig.data:
                trace.error_y = dict(
                    type="data",
                    array=kwargs["error_y"],
                    visible=True
                )

        return fig

    def _create_scatter_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced scatter plot with additional features."""
        fig = px.scatter(
            data,
            x=x,
            y=y,
            **kwargs
        )

        # Add trend line if requested
        if kwargs.get("show_trend", False):
            self._add_trend_line(fig, data[x], data[y], "Trend")

        # Add confidence intervals if requested
        if kwargs.get("show_ci", False):
            self._add_confidence_intervals(fig, data[x], data[y])

        return fig

    def _create_histogram(
        self,
        data: pd.DataFrame,
        x: str,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced histogram with density curve."""
        fig = px.histogram(
            data,
            x=x,
            **kwargs
        )

        # Add KDE curve if requested
        if kwargs.get("show_kde", False):
            kde = sns.kdeplot(data=data[x].dropna())
            line_data = kde.get_lines()[0].get_data()
            fig.add_trace(
                go.Scatter(
                    x=line_data[0],
                    y=line_data[1],
                    name="Density",
                    line=dict(color="red")
                )
            )

        return fig

    def _create_box_plot(
        self,
        data: pd.DataFrame,
        x: Optional[str],
        y: str,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced box plot with optional grouping."""
        fig = px.box(
            data,
            x=x,
            y=y,
            **kwargs
        )

        # Add individual points if requested
        if kwargs.get("show_points", False):
            fig.update_traces(
                points="all",
                jitter=0.3,
                pointpos=-1.8
            )

        return fig

    def _create_violin_plot(
        self,
        data: pd.DataFrame,
        x: Optional[str],
        y: str,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced violin plot with box plot overlay."""
        fig = px.violin(
            data,
            x=x,
            y=y,
            **kwargs
        )

        # Add box plot overlay if requested
        if kwargs.get("show_box", True):
            fig.update_traces(
                box_visible=True,
                meanline_visible=True
            )

        return fig

    def _create_heatmap(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced heatmap with customizable features."""
        correlation = kwargs.get("correlation", True)
        if correlation:
            matrix = data.corr()
        else:
            matrix = data

        fig = px.imshow(
            matrix,
            color_continuous_scale=kwargs.get("color_scale", "RdBu_r"),
            **kwargs
        )

        # Add text annotations if requested
        if kwargs.get("show_values", True):
            fig.update_traces(
                text=matrix.round(2),
                texttemplate="%{text}"
            )

        return fig

    def _create_pie_chart(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced pie chart with customizable features."""
        values = kwargs.pop("values")
        names = kwargs.pop("names")

        fig = px.pie(
            data,
            values=values,
            names=names,
            **kwargs
        )

        # Add percentage labels if requested
        if kwargs.get("show_percentage", True):
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

        return fig

    def _create_area_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        **kwargs
    ) -> go.Figure:
        """Create an enhanced area plot with multiple series support."""
        if isinstance(y, str):
            fig = px.area(
                data,
                x=x,
                y=y,
                **kwargs
            )
        else:
            fig = go.Figure()
            for y_col in y:
                fig.add_trace(
                    go.Scatter(
                        x=data[x],
                        y=data[y_col],
                        name=y_col,
                        fill="tonexty"
                    )
                )

        return fig

    def _create_parallel_coordinates(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced parallel coordinates plot."""
        dimensions = kwargs.pop("dimensions", data.columns.tolist())
        fig = px.parallel_coordinates(
            data,
            dimensions=dimensions,
            **kwargs
        )

        return fig

    def _create_scatter_matrix(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced scatter matrix with customizable features."""
        dimensions = kwargs.pop("dimensions", data.select_dtypes(include=[np.number]).columns)
        fig = px.scatter_matrix(
            data,
            dimensions=dimensions,
            **kwargs
        )

        return fig

    def _create_sunburst(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced sunburst diagram."""
        path = kwargs.pop("path")
        values = kwargs.pop("values", None)

        fig = px.sunburst(
            data,
            path=path,
            values=values,
            **kwargs
        )

        return fig

    def _create_distribution_plot(
        self,
        data: pd.DataFrame,
        x: str,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced distribution plot with multiple components."""
        fig = ff.create_distplot(
            [data[x].dropna()],
            [x],
            show_hist=kwargs.get("show_hist", True),
            show_curve=kwargs.get("show_curve", True),
            show_rug=kwargs.get("show_rug", True)
        )

        return fig

    def _create_bubble_plot(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced bubble plot."""
        x = kwargs.pop("x")
        y = kwargs.pop("y")
        size = kwargs.pop("size")
        color = kwargs.pop("color", None)

        fig = px.scatter(
            data,
            x=x,
            y=y,
            size=size,
            color=color,
            **kwargs
        )

        return fig

    def _create_radar_plot(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced radar plot."""
        categories = kwargs.pop("categories")
        values = kwargs.pop("values")

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself"
        ))

        return fig

    def _create_treemap(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced treemap visualization."""
        path = kwargs.pop("path")
        values = kwargs.pop("values", None)

        fig = px.treemap(
            data,
            path=path,
            values=values,
            **kwargs
        )

        return fig

    def _create_funnel_plot(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> go.Figure:
        """Create an enhanced funnel plot."""
        x = kwargs.pop("x")
        y = kwargs.pop("y")

        fig = go.Figure(go.Funnel(
            x=data[x],
            y=data[y],
            **kwargs
        ))

        return fig

    def _add_trend_line(
        self,
        fig: go.Figure,
        x: pd.Series,
        y: pd.Series,
        name: str
    ) -> None:
        """Add a trend line to the figure."""
        z = np.polyfit(range(len(x)), y, 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=p(range(len(x))),
                name=f"{name} Trend",
                line=dict(dash="dash")
            )
        )

    def _add_confidence_intervals(
        self,
        fig: go.Figure,
        x: pd.Series,
        y: pd.Series,
        confidence: float = 0.95
    ) -> None:
        """Add confidence intervals to the figure."""
        from scipy import stats

        slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(x)), y)
        y_pred = slope * np.arange(len(x)) + intercept
        
        # Calculate confidence intervals
        conf_int = std_err * stats.t.ppf((1 + confidence) / 2, len(x) - 2)
        lower = y_pred - conf_int
        upper = y_pred + conf_int

        fig.add_trace(
            go.Scatter(
                x=x,
                y=upper,
                mode="lines",
                line=dict(width=0),
                showlegend=False
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=lower,
                mode="lines",
                line=dict(width=0),
                fillcolor="rgba(68, 68, 68, 0.3)",
                fill="tonexty",
                showlegend=False
            )
        )

    def _apply_styling(self, fig: go.Figure, **kwargs) -> None:
        """Apply common styling to the figure."""
        title = kwargs.get("title", "")
        x_label = kwargs.get("x_label", "")
        y_label = kwargs.get("y_label", "")

        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor="center"
            ),
            xaxis_title=x_label,
            yaxis_title=y_label,
            template=self.theme,
            showlegend=kwargs.get("show_legend", True),
            height=kwargs.get("height", 600),
            width=kwargs.get("width", 800)
        )

        # Apply custom theme if specified
        if "theme" in kwargs:
            fig.update_layout(template=kwargs["theme"])

        # Apply custom colors if specified
        if "colors" in kwargs:
            fig.update_traces(marker_color=kwargs["colors"])

    def _convert_to_json(self, fig: go.Figure) -> str:
        """Convert the figure to JSON format."""
        return fig.to_json()

    def analyze_and_visualize(
        self,
        data: pd.DataFrame,
        analysis_type: str,
        **kwargs
    ) -> List[Dict]:
        """Analyze data and create appropriate visualizations."""
        try:
            visualizations = []

            if analysis_type == "distribution":
                for col in data.select_dtypes(include=[np.number]).columns:
                    viz = self.create_visualization(
                        data,
                        "histogram",
                        x=col,
                        title=f"Distribution of {col}",
                        show_kde=True
                    )
                    visualizations.append(viz)

            elif analysis_type == "correlation":
                viz = self.create_visualization(
                    data,
                    "heatmap",
                    correlation=True,
                    title="Correlation Matrix",
                    show_values=True
                )
                visualizations.append(viz)

            elif analysis_type == "time_series":
                date_col = kwargs.get("date_column")
                if date_col:
                    for col in data.select_dtypes(include=[np.number]).columns:
                        viz = self.create_visualization(
                            data,
                            "line",
                            x=date_col,
                            y=col,
                            title=f"Time Series of {col}",
                            show_trend=True
                        )
                        visualizations.append(viz)

            elif analysis_type == "comparison":
                categorical_col = kwargs.get("category_column")
                if categorical_col:
                    for col in data.select_dtypes(include=[np.number]).columns:
                        viz = self.create_visualization(
                            data,
                            "box",
                            x=categorical_col,
                            y=col,
                            title=f"Comparison of {col} by {categorical_col}",
                            show_points=True
                        )
                        visualizations.append(viz)

            return visualizations

        except Exception as e:
            self.logger.error(f"Error in analyze_and_visualize: {str(e)}")
            raise 