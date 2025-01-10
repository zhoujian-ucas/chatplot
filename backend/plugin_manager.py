from typing import Dict, List, Optional, Type
import logging
import os
from .plugins.base import PluginManager, PluginInterface, PluginMetadata
from .plugins.base import DataProcessorPlugin, VisualizationPlugin, AnalysisPlugin, ModelPlugin

class ChatPlotPluginManager:
    """Manages plugins for the ChatPlot application."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.plugin_manager = PluginManager()
        self.plugin_types = {
            "data_processor": DataProcessorPlugin,
            "visualization": VisualizationPlugin,
            "analysis": AnalysisPlugin,
            "model": ModelPlugin
        }
    
    def initialize(self, plugins_dir: str = "plugins") -> None:
        """Initialize the plugin system."""
        try:
            # Create plugins directory if it doesn't exist
            os.makedirs(plugins_dir, exist_ok=True)
            
            # Load plugins from directory
            self.plugin_manager.load_plugins_from_directory(plugins_dir)
            
            self.logger.info(f"Successfully initialized plugin system with {len(self.plugin_manager.list_plugins())} plugins")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize plugin system: {str(e)}")
            raise
    
    def get_plugins_by_type(self, plugin_type: str) -> List[PluginMetadata]:
        """Get all plugins of a specific type."""
        if plugin_type not in self.plugin_types:
            raise ValueError(f"Unknown plugin type: {plugin_type}")
        
        base_class = self.plugin_types[plugin_type]
        return [
            plugin.metadata for plugin in self.plugin_manager.plugins.values()
            if isinstance(plugin, base_class)
        ]
    
    def process_data(self, plugin_name: str, data: any, **kwargs) -> Dict:
        """Process data using a data processor plugin."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not isinstance(plugin, DataProcessorPlugin):
            raise ValueError(f"Plugin {plugin_name} is not a data processor plugin")
        
        try:
            return plugin.process_data(data, **kwargs)
        except Exception as e:
            self.logger.error(f"Error processing data with plugin {plugin_name}: {str(e)}")
            raise
    
    def create_visualization(self, plugin_name: str, data: any, **kwargs) -> Dict:
        """Create visualization using a visualization plugin."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not isinstance(plugin, VisualizationPlugin):
            raise ValueError(f"Plugin {plugin_name} is not a visualization plugin")
        
        try:
            return plugin.create_visualization(data, **kwargs)
        except Exception as e:
            self.logger.error(f"Error creating visualization with plugin {plugin_name}: {str(e)}")
            raise
    
    def analyze_data(self, plugin_name: str, data: any, **kwargs) -> Dict:
        """Analyze data using an analysis plugin."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not isinstance(plugin, AnalysisPlugin):
            raise ValueError(f"Plugin {plugin_name} is not an analysis plugin")
        
        try:
            return plugin.analyze_data(data, **kwargs)
        except Exception as e:
            self.logger.error(f"Error analyzing data with plugin {plugin_name}: {str(e)}")
            raise
    
    def train_model(self, plugin_name: str, data: any, **kwargs) -> None:
        """Train a model using a model plugin."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not isinstance(plugin, ModelPlugin):
            raise ValueError(f"Plugin {plugin_name} is not a model plugin")
        
        try:
            plugin.train(data, **kwargs)
        except Exception as e:
            self.logger.error(f"Error training model with plugin {plugin_name}: {str(e)}")
            raise
    
    def predict_with_model(self, plugin_name: str, data: any, **kwargs) -> Dict:
        """Make predictions using a model plugin."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not isinstance(plugin, ModelPlugin):
            raise ValueError(f"Plugin {plugin_name} is not a model plugin")
        
        try:
            return plugin.predict(data, **kwargs)
        except Exception as e:
            self.logger.error(f"Error making predictions with plugin {plugin_name}: {str(e)}")
            raise
    
    def get_plugin_config(self, plugin_name: str) -> Optional[Dict]:
        """Get plugin configuration."""
        return self.plugin_manager.get_plugin_config(plugin_name)
    
    def update_plugin_config(self, plugin_name: str, config: Dict) -> None:
        """Update plugin configuration."""
        try:
            self.plugin_manager.update_plugin_config(plugin_name, config)
        except Exception as e:
            self.logger.error(f"Error updating configuration for plugin {plugin_name}: {str(e)}")
            raise
    
    def reload_plugin(self, plugin_name: str) -> None:
        """Reload a plugin."""
        try:
            self.plugin_manager.reload_plugin(plugin_name)
        except Exception as e:
            self.logger.error(f"Error reloading plugin {plugin_name}: {str(e)}")
            raise
    
    def get_plugin_metadata(self, plugin_name: str) -> PluginMetadata:
        """Get plugin metadata."""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        return plugin.metadata 