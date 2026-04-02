plugin_registry = {}

def register_plugin(cls):
    plugin_registry[cls.name] = cls
    return cls