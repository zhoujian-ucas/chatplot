import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from typing import Dict, Any, List, Optional, Tuple
import logging
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

class VisualizationService:
    def __init__(self):
        # Set default styles
        plt.style.use('seaborn')
        sns.set_palette("husl")
        self.default_colors = px.colors.qualitative.Set3
        self.theme = "plotly_white"

    def create_visualization(
        self,
        data: pd.DataFrame,
        viz_type: str,
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: Optional[str] = None,
        interactive: bool = True,
        **kwargs
    ) -> str:
        """
        Create visualization with support for both static and interactive plots
        """
        try:
            if interactive:
                fig = self._create_interactive_plot(
                    data, viz_type, x_column, y_column, title, **kwargs
                )
                return self._convert_plotly_to_html(fig)
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                self._create_static_plot(
                    data, viz_type, x_column, y_column, title, ax, **kwargs
                )
                return self._convert_plot_to_base64(fig)

        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise

    def create_multiple_visualizations(
        self,
        data: pd.DataFrame,
        viz_configs: List[Dict[str, Any]],
        layout: Optional[Tuple[int, int]] = None
    ) -> str:
        """
        Create multiple visualizations in a grid layout
        """
        try:
            n_plots = len(viz_configs)
            if layout is None:
                n_rows = int(np.ceil(np.sqrt(n_plots)))
                n_cols = int(np.ceil(n_plots / n_rows))
            else:
                n_rows, n_cols = layout

            fig = make_subplots(
                rows=n_rows,
                cols=n_cols,
                subplot_titles=[config.get('title', '') for config in viz_configs]
            )

            for i, config in enumerate(viz_configs):
                row = i // n_cols + 1
                col = i % n_cols + 1
                
                plot = self._create_interactive_plot(
                    data,
                    config['type'],
                    config.get('x_column'),
                    config.get('y_column'),
                    config.get('title'),
                    **config.get('kwargs', {})
                )
                
                for trace in plot.data:
                    fig.add_trace(trace, row=row, col=col)

            fig.update_layout(
                height=400 * n_rows,
                width=600 * n_cols,
                showlegend=True,
                template=self.theme
            )

            return self._convert_plotly_to_html(fig)

        except Exception as e:
            logger.error(f"Error creating multiple visualizations: {str(e)}")
            raise

    def _create_interactive_plot(
        self,
        data: pd.DataFrame,
        viz_type: str,
        x_column: Optional[str],
        y_column: Optional[str],
        title: Optional[str],
        **kwargs
    ) -> go.Figure:
        """
        Create interactive Plotly visualization
        """
        if viz_type == "line":
            fig = px.line(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "bar":
            fig = px.bar(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "scatter":
            fig = px.scatter(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "histogram":
            fig = px.histogram(data, x=x_column, title=title, **kwargs)
        elif viz_type == "box":
            fig = px.box(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "violin":
            fig = px.violin(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "heatmap":
            fig = px.imshow(
                data.corr() if kwargs.get('correlation', True) else data,
                title=title,
                **kwargs
            )
        elif viz_type == "scatter_matrix":
            fig = px.scatter_matrix(
                data,
                dimensions=kwargs.get('dimensions', data.select_dtypes(include=[np.number]).columns),
                title=title
            )
        elif viz_type == "parallel_coordinates":
            fig = px.parallel_coordinates(
                data,
                dimensions=kwargs.get('dimensions', data.select_dtypes(include=[np.number]).columns),
                title=title
            )
        elif viz_type == "area":
            fig = px.area(data, x=x_column, y=y_column, title=title, **kwargs)
        elif viz_type == "pie":
            fig = px.pie(data, values=y_column, names=x_column, title=title, **kwargs)
        elif viz_type == "sunburst":
            fig = px.sunburst(
                data,
                path=kwargs.get('path', [x_column]),
                values=y_column,
                title=title
            )
        else:
            raise ValueError(f"Unsupported visualization type: {viz_type}")

        fig.update_layout(template=self.theme)
        return fig

    def _create_static_plot(
        self,
        data: pd.DataFrame,
        viz_type: str,
        x_column: Optional[str],
        y_column: Optional[str],
        title: Optional[str],
        ax: plt.Axes,
        **kwargs
    ) -> None:
        """
        Create static Matplotlib/Seaborn visualization
        """
        if viz_type == "line":
            sns.lineplot(data=data, x=x_column, y=y_column, ax=ax, **kwargs)
        elif viz_type == "bar":
            sns.barplot(data=data, x=x_column, y=y_column, ax=ax, **kwargs)
        elif viz_type == "scatter":
            sns.scatterplot(data=data, x=x_column, y=y_column, ax=ax, **kwargs)
        elif viz_type == "histogram":
            sns.histplot(data=data[x_column], ax=ax, **kwargs)
        elif viz_type == "box":
            sns.boxplot(data=data, x=x_column, y=y_column, ax=ax, **kwargs)
        elif viz_type == "violin":
            sns.violinplot(data=data, x=x_column, y=y_column, ax=ax, **kwargs)
        elif viz_type == "heatmap":
            sns.heatmap(
                data.corr() if kwargs.get('correlation', True) else data,
                ax=ax,
                **kwargs
            )
        elif viz_type == "kde":
            sns.kdeplot(data=data[x_column], ax=ax, **kwargs)
        else:
            raise ValueError(f"Unsupported visualization type: {viz_type}")

        if title:
            ax.set_title(title)

    def _convert_plot_to_base64(self, fig: plt.Figure) -> str:
        """
        Convert matplotlib figure to base64 string
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return image_base64

    def _convert_plotly_to_html(self, fig: go.Figure) -> str:
        """
        Convert Plotly figure to HTML string
        """
        return fig.to_html(
            full_html=False,
            include_plotlyjs='cdn',
            config={'responsive': True}
        )

    def analyze_and_visualize(
        self,
        data: pd.DataFrame,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive visualization based on analysis results
        """
        try:
            viz_type = analysis_result.get("visualization_type", "bar")
            numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns

            if not numeric_columns.empty:
                y_column = numeric_columns[0]
                x_column = data.columns[0] if data.columns[0] != y_column else data.columns[1]

                # Create main visualization
                main_chart = self.create_visualization(
                    data,
                    viz_type,
                    x_column=x_column,
                    y_column=y_column,
                    title=f"{viz_type.capitalize()} Chart of {y_column} by {x_column}",
                    interactive=True
                )

                # Create additional visualizations based on analysis
                additional_charts = []
                if analysis_result.get("suggested_visualizations"):
                    additional_charts = [
                        self.create_visualization(
                            data,
                            viz['type'],
                            x_column=viz['columns'][0] if len(viz['columns']) > 0 else None,
                            y_column=viz['columns'][1] if len(viz['columns']) > 1 else None,
                            title=viz['title'],
                            interactive=True
                        )
                        for viz in analysis_result["suggested_visualizations"]
                    ]

                return {
                    "main_chart": main_chart,
                    "additional_charts": additional_charts,
                    "analysis": analysis_result,
                    "metadata": {
                        "x_column": x_column,
                        "y_column": y_column,
                        "viz_type": viz_type
                    }
                }
            else:
                raise ValueError("No numeric columns found in the data")

        except Exception as e:
            logger.error(f"Error in analyze_and_visualize: {str(e)}")
            raise 