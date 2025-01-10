from typing import Any, Dict, List, Optional
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from ..base import PluginMetadata, VisualizationPlugin

class WaterfallChartPlugin(VisualizationPlugin):
    """A plugin that creates waterfall charts for financial or cumulative data analysis."""
    
    def __init__(self):
        self._config = {}
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="waterfall_chart",
            version="1.0.0",
            description="Creates waterfall charts for visualizing cumulative changes",
            author="ChatPlot",
            dependencies=["plotly", "pandas", "numpy"],
            entry_point="WaterfallChartPlugin",
            config_schema={
                "type": "object",
                "properties": {
                    "colors": {
                        "type": "object",
                        "properties": {
                            "positive": {"type": "string"},
                            "negative": {"type": "string"},
                            "total": {"type": "string"}
                        }
                    },
                    "show_totals": {"type": "boolean"},
                    "show_connectors": {"type": "boolean"}
                }
            }
        )
    
    def initialize(self, config: Optional[Dict] = None) -> None:
        """Initialize the plugin with configuration."""
        default_config = {
            "colors": {
                "positive": "#00876c",
                "negative": "#e63946",
                "total": "#457b9d"
            },
            "show_totals": True,
            "show_connectors": True
        }
        self._config = {**default_config, **(config or {})}
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass
    
    def create_visualization(self, data: Any, **kwargs) -> Dict:
        """Create a waterfall chart visualization."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        # Extract required columns
        categories = kwargs.get("categories", data.columns[0])
        values = kwargs.get("values", data.columns[1])
        
        if categories not in data.columns or values not in data.columns:
            raise ValueError("Specified columns not found in DataFrame")
        
        # Prepare data
        df = data[[categories, values]].copy()
        df["cumulative"] = df[values].cumsum()
        df["previous"] = df["cumulative"].shift(1)
        df["direction"] = df[values] >= 0
        
        # Create figure
        fig = go.Figure()
        
        # Add bars
        for idx, row in df.iterrows():
            color = (self._config["colors"]["positive"] if row["direction"]
                    else self._config["colors"]["negative"])
            
            fig.add_trace(go.Waterfall(
                name=str(row[categories]),
                orientation="v",
                measure=["relative"],
                x=[idx],
                y=[row[values]],
                connector={
                    "line": {
                        "color": "rgb(63, 63, 63)",
                        "width": 1,
                        "dash": "solid"
                    }
                },
                decreasing={
                    "marker": {"color": self._config["colors"]["negative"]}
                },
                increasing={
                    "marker": {"color": self._config["colors"]["positive"]}
                },
                totals={
                    "marker": {"color": self._config["colors"]["total"]}
                }
            ))
        
        # Add total bar if configured
        if self._config["show_totals"]:
            fig.add_trace(go.Waterfall(
                name="Total",
                orientation="v",
                measure=["total"],
                x=[len(df)],
                y=[df[values].sum()],
                connector={
                    "line": {
                        "color": "rgb(63, 63, 63)",
                        "width": 1,
                        "dash": "solid"
                    }
                },
                decreasing={
                    "marker": {"color": self._config["colors"]["negative"]}
                },
                increasing={
                    "marker": {"color": self._config["colors"]["positive"]}
                },
                totals={
                    "marker": {"color": self._config["colors"]["total"]}
                }
            ))
        
        # Update layout
        fig.update_layout(
            title=kwargs.get("title", "Waterfall Chart"),
            showlegend=False,
            xaxis_title=kwargs.get("x_label", categories),
            yaxis_title=kwargs.get("y_label", values),
            waterfallgap=0.2,
            template="plotly_white"
        )
        
        # Customize connector lines
        if not self._config["show_connectors"]:
            fig.update_traces(connector={"visible": False})
        
        return {
            "plot": fig.to_json(),
            "type": "waterfall",
            "parameters": {
                "categories": categories,
                "values": values,
                **kwargs
            }
        } 