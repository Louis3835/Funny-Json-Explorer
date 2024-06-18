from abc import ABC, abstractmethod
from ..icon import IconFamily
from ..node import JsonNode

class StyleJsonNode(ABC):
    def __init__(self, json_node: JsonNode, icon_family: IconFamily):
        self.json_node = json_node
        self.icon_family = icon_family

    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def accept(self):
        pass

# 抽象工厂：创建 StyleJsonNode
class StyleJsonNodeFactory(ABC):
    @abstractmethod
    def create_style_json_node(self, json_node: JsonNode, icon_family: IconFamily) -> StyleJsonNode:
        pass

