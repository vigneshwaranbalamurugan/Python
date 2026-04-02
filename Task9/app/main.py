import argparse
from .plugin_manager import PluginManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("--theme")
    args = parser.parse_args()

    manager = PluginManager()
    manager.discover_local_plugins()
    manager.discover_entrypoint_plugins()
    manager.resolve_dependencies()
    manager.activate_plugins()

    if args.theme:
        plugin = manager.plugins.get(args.theme)
        if plugin:
            plugin.activate()
        else:
            print("Theme not found")
    manager.deactivate_plugins()
            
if __name__ == "__main__":
    main()
    