from app.plugin_base import PluginBase
from app.registry import register_plugin

@register_plugin
class LightThemePlugin(PluginBase):
    name = "light_theme_plugin"
    dependencies = []

    def activate(self):
        print(1/0)
        print("Light theme activated")

    def deactivate(self):
        print("Light theme deactivated")