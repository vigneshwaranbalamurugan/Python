from app.plugin_base import PluginBase
from app.registry import register_plugin

@register_plugin
class ReactPlugin(PluginBase):
    name = "react_app_plugin"
    dependencies = ["node_app_plugin"]

    def activate(self):
        print("React app activated")

    def deactivate(self):
        print("React app deactivated")