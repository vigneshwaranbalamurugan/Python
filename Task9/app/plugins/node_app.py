from app.plugin_base import PluginBase
from app.registry import register_plugin

@register_plugin
class NodePlugin(PluginBase):
    name = "node_app_plugin"
    dependencies = []

    def activate(self):
        print("Node app activated")

    def deactivate(self):
        print("Node app deactivated")