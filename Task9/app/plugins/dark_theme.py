from app.plugin_base import PluginBase
from app.registry import register_plugin

@register_plugin
class DarkThemePlugin(PluginBase):
    name = "dark_theme_plugin"
    dependencies = []

    def activate(self):
        print("Dark theme activated")

    def deactivate(self):
        print("Dark theme deactivated")