from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
import logging
from dataclasses import dataclass
import importlib
import inspect
import os
import yaml

@dataclass
class PluginMetadata:
    """Plugin metadata information."""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]
    entry_point: str
    config_schema: Optional[Dict] = None

class PluginInterface(ABC):
    """Base interface that all plugins must implement."""
    
    @abstractmethod
    def initialize(self, config: Optional[Dict] = None) -> None:
        """Initialize the plugin with optional configuration."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Clean up resources when plugin is being unloaded."""
        pass
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass

class DataProcessorPlugin(PluginInterface):
    """Interface for plugins that process data."""
    
    @abstractmethod
    def process_data(self, data: Any, **kwargs) -> Any:
        """Process input data and return processed result."""
        pass

class VisualizationPlugin(PluginInterface):
    """Interface for plugins that create visualizations."""
    
    @abstractmethod
    def create_visualization(self, data: Any, **kwargs) -> Dict:
        """Create visualization from input data."""
        pass

class AnalysisPlugin(PluginInterface):
    """Interface for plugins that perform data analysis."""
    
    @abstractmethod
    def analyze_data(self, data: Any, **kwargs) -> Dict:
        """Analyze input data and return results."""
        pass

class ModelPlugin(PluginInterface):
    """Interface for plugins that provide machine learning models."""
    
    @abstractmethod
    def train(self, data: Any, **kwargs) -> None:
        """Train the model on input data."""
        pass
    
    @abstractmethod
    def predict(self, data: Any, **kwargs) -> Any:
        """Make predictions using the trained model."""
        pass

class PluginManager:
    """Manages plugin lifecycle and registration."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_configs: Dict[str, Dict] = {}
    
    def register_plugin(self, plugin_class: Type[PluginInterface], config: Optional[Dict] = None) -> None:
        """Register a new plugin."""
        try:
            plugin = plugin_class()
            metadata = plugin.metadata
            
            if metadata.name in self.plugins:
                raise ValueError(f"Plugin {metadata.name} is already registered")
            
            # Validate dependencies
            self._validate_dependencies(metadata.dependencies)
            
            # Initialize plugin
            plugin.initialize(config)
            
            # Store plugin and its configuration
            self.plugins[metadata.name] = plugin
            if config:
                self.plugin_configs[metadata.name] = config
            
            self.logger.info(f"Successfully registered plugin: {metadata.name} v{metadata.version}")
            
        except Exception as e:
            self.logger.error(f"Failed to register plugin: {str(e)}")
            raise
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """Unregister a plugin."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.shutdown()
            del self.plugins[plugin_name]
            if plugin_name in self.plugin_configs:
                del self.plugin_configs[plugin_name]
            
            self.logger.info(f"Successfully unregistered plugin: {plugin_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to unregister plugin: {str(e)}")
            raise
    
    def get_plugin(self, plugin_name: str) -> PluginInterface:
        """Get a registered plugin by name."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        return self.plugins[plugin_name]
    
    def list_plugins(self) -> List[PluginMetadata]:
        """List all registered plugins."""
        return [plugin.metadata for plugin in self.plugins.values()]
    
    def load_plugins_from_directory(self, directory: str) -> None:
        """Load plugins from a directory."""
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        plugin_path = os.path.join(root, file)
                        self._load_plugin_from_file(plugin_path)
                        
        except Exception as e:
            self.logger.error(f"Failed to load plugins from directory: {str(e)}")
            raise
    
    def _load_plugin_from_file(self, plugin_path: str) -> None:
        """Load a plugin from a Python file."""
        try:
            # Get module name from file path
            module_name = os.path.splitext(os.path.basename(plugin_path))[0]
            
            # Load module
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load plugin from {plugin_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginInterface) and 
                    obj != PluginInterface):
                    
                    # Load configuration if exists
                    config_path = os.path.join(os.path.dirname(plugin_path), 'config.yaml')
                    config = None
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = yaml.safe_load(f)
                    
                    # Register plugin
                    self.register_plugin(obj, config)
                    
        except Exception as e:
            self.logger.error(f"Failed to load plugin from {plugin_path}: {str(e)}")
            raise
    
    def _validate_dependencies(self, dependencies: List[str]) -> None:
        """Validate plugin dependencies."""
        missing_deps = []
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            raise ImportError(f"Missing dependencies: {', '.join(missing_deps)}")

    def reload_plugin(self, plugin_name: str) -> None:
        """Reload a plugin."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        
        try:
            # Get plugin and its config
            plugin = self.plugins[plugin_name]
            config = self.plugin_configs.get(plugin_name)
            
            # Unregister old instance
            self.unregister_plugin(plugin_name)
            
            # Register new instance
            plugin_class = type(plugin)
            self.register_plugin(plugin_class, config)
            
            self.logger.info(f"Successfully reloaded plugin: {plugin_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to reload plugin: {str(e)}")
            raise

    def get_plugin_config(self, plugin_name: str) -> Optional[Dict]:
        """Get plugin configuration."""
        return self.plugin_configs.get(plugin_name)

    def update_plugin_config(self, plugin_name: str, config: Dict) -> None:
        """Update plugin configuration."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.initialize(config)
            self.plugin_configs[plugin_name] = config
            
            self.logger.info(f"Successfully updated configuration for plugin: {plugin_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to update plugin configuration: {str(e)}")
            raise 