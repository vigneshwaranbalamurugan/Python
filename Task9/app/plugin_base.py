from abc import ABC, abstractmethod

class PluginBase(ABC):
    name = ""
    dependencies = []

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass