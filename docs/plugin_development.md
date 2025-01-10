# ChatPlot Plugin Development Guide

## Overview

ChatPlot's plugin system allows developers to extend the application's functionality by creating custom plugins for:
- Data Processing
- Visualization
- Data Analysis
- Machine Learning Models

This guide will walk you through the process of creating and integrating plugins into ChatPlot.

## Plugin Types

### 1. Data Processor Plugins
Process and transform data in various ways. Examples include:
- Data cleaning
- Feature engineering
- Time series processing
- Text preprocessing

### 2. Visualization Plugins
Create custom visualizations. Examples include:
- Custom chart types
- Interactive visualizations
- Specialized plots
- Multi-dimensional visualizations

### 3. Analysis Plugins
Implement data analysis algorithms. Examples include:
- Statistical analysis
- Pattern recognition
- Market basket analysis
- Clustering analysis

### 4. Model Plugins
Implement machine learning models. Examples include:
- Classification models
- Regression models
- Anomaly detection
- Time series forecasting

## Plugin Structure

Each plugin must implement one of the base plugin interfaces and include:

1. Metadata
```python
@property
def metadata(self) -> PluginMetadata:
    return PluginMetadata(
        name="my_plugin",
        version="1.0.0",
        description="Plugin description",
        author="Author name",
        dependencies=["required", "packages"],
        entry_point="PluginClassName",
        config_schema={
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "number"}
            }
        }
    )
```

2. Initialization
```python
def initialize(self, config: Optional[Dict] = None) -> None:
    default_config = {
        "param1": "default_value",
        "param2": 42
    }
    self._config = {**default_config, **(config or {})}
```

3. Core functionality (depending on plugin type)
```python
# For DataProcessorPlugin
def process_data(self, data: Any, **kwargs) -> Any:
    # Implementation

# For VisualizationPlugin
def create_visualization(self, data: Any, **kwargs) -> Dict:
    # Implementation

# For AnalysisPlugin
def analyze_data(self, data: Any, **kwargs) -> Dict:
    # Implementation

# For ModelPlugin
def train(self, data: Any, **kwargs) -> None:
    # Implementation

def predict(self, data: Any, **kwargs) -> Any:
    # Implementation
```

## Creating a Plugin

1. Create a new Python file in the `plugins` directory
2. Import required base classes
3. Implement the plugin class
4. Create a configuration file (optional)

Example:
```python
from typing import Any, Dict, Optional
from ..base import PluginMetadata, DataProcessorPlugin

class MyPlugin(DataProcessorPlugin):
    def __init__(self):
        self._config = {}
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(...)
    
    def initialize(self, config: Optional[Dict] = None) -> None:
        # Implementation
    
    def process_data(self, data: Any, **kwargs) -> Any:
        # Implementation
```

## Configuration

Plugins can be configured using YAML files:

```yaml
my_plugin:
  param1: "value1"
  param2: 42
  nested:
    param3: "value3"
```

## Best Practices

1. Error Handling
- Handle exceptions gracefully
- Provide meaningful error messages
- Log errors appropriately

```python
try:
    # Implementation
except Exception as e:
    self.logger.error(f"Error in plugin: {str(e)}")
    raise
```

2. Input Validation
- Validate input data types
- Check required parameters
- Verify data format

```python
if not isinstance(data, pd.DataFrame):
    raise ValueError("Input must be a pandas DataFrame")

if required_param not in kwargs:
    raise ValueError("Missing required parameter")
```

3. Documentation
- Document plugin purpose and functionality
- Describe parameters and return values
- Provide usage examples

4. Testing
- Write unit tests
- Test edge cases
- Verify error handling

## Integration

1. Install Dependencies
```bash
pip install -r requirements.txt
```

2. Place Plugin Files
```
plugins/
  ├── my_plugin.py
  └── config.yaml
```

3. Register Plugin
The plugin will be automatically registered when ChatPlot starts.

## Example Plugins

See the `examples` directory for sample plugins:
- `waterfall_chart.py`: Custom visualization plugin
- `time_series_processor.py`: Data processing plugin
- `market_basket_analyzer.py`: Analysis plugin
- `anomaly_detector.py`: Model plugin

## API Reference

### PluginMetadata
| Field | Type | Description |
|-------|------|-------------|
| name | str | Plugin name |
| version | str | Plugin version |
| description | str | Plugin description |
| author | str | Plugin author |
| dependencies | List[str] | Required packages |
| entry_point | str | Plugin class name |
| config_schema | Optional[Dict] | Configuration schema |

### Plugin Interfaces
| Interface | Main Methods | Purpose |
|-----------|-------------|----------|
| DataProcessorPlugin | process_data | Data transformation |
| VisualizationPlugin | create_visualization | Custom charts |
| AnalysisPlugin | analyze_data | Data analysis |
| ModelPlugin | train, predict | Machine learning |

## Troubleshooting

Common issues and solutions:

1. Plugin Not Loading
- Check file location
- Verify dependencies
- Check syntax errors

2. Configuration Issues
- Validate YAML syntax
- Check schema compliance
- Verify file permissions

3. Runtime Errors
- Check input data format
- Verify parameter types
- Review error logs

## Support

For help with plugin development:
1. Check documentation
2. Review example plugins
3. Submit issues on GitHub
4. Join community discussions 