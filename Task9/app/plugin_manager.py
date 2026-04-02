import importlib
import os

from importlib.metadata import entry_points
from .plugin_base import PluginBase
from .registry import plugin_registry


class PluginManager:
    def __init__(self, plugin_folder="app.plugins"):
        self.plugin_folder = plugin_folder
        self.plugins = {}
        self.activation_order = []

    def discover_local_plugins(self):
        plugin_folder_path = os.path.join(os.path.dirname(__file__), "plugins")
        for file in os.listdir(plugin_folder_path):
            if file.endswith(".py"):
                module_name = file[:-3]
                module = importlib.import_module(f"{self.plugin_folder}.{module_name}")
        for name, cls in plugin_registry.items():
            self.plugins[name] = cls()
        
    def discover_entrypoint_plugins(self):
        eps = entry_points(group="plugins")
        for ep in eps:
            plugin_class = ep.load()
            plugin_instance = plugin_class()
            self.plugins[plugin_instance.name] = plugin_instance

    def resolve_dependencies(self):
        visited = set()
        stack = set()
        def visit(plugin):
            if plugin.name in stack:
                raise Exception("Circular dependency detected")

            if plugin.name not in visited:
                stack.add(plugin.name)
                for dependency in plugin.dependencies:
                    if dependency not in self.plugins:
                        raise Exception(
                            f"Missing dependency: {dependency}"
                        )
                    visit(self.plugins[dependency])
                stack.remove(plugin.name)
                visited.add(plugin.name)
                self.activation_order.append(plugin)

        for plugin in self.plugins.values():
            visit(plugin)

    def activate_plugins(self):
        for plugin in self.activation_order:
            try:
                plugin.activate()
            except Exception as error:
                print(
                    f"Plugin {plugin.name} failed: {error}"
                )
    
    def deactivate_plugins(self):
        for plugin in self.activation_order:
            try:
                plugin.deactivate()
            except Exception as error:
                print(
                    f"Plugin {plugin.name} deactivation failed: {error}"
                )