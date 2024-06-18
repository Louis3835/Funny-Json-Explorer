from abc import ABC, abstractmethod
from typing import List, Callable, Union
import json
import os

from .Exception import FileException

id_counter = 0

# 1. 访问模式：被访问元素
# 2. 组件模式
class JsonNode:
    def __init__(self, name, level):
        global id_counter
        self.name = name
        self.level = level
        self.id = id_counter
        id_counter += 1

    #是否是叶节点
    @abstractmethod
    def is_leaf(self):
        raise NotImplementedError("Must be implemented by the subclass.")

    # 是否是根节点
    def is_root(self):
        return self.level == 0

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_level(self):
        return self.level
    
    # 深度优先遍历节点
    @abstractmethod
    def dfs(self):
        raise NotImplementedError("Must be implemented by the subclass.")

    # 访问者模式：被访问元素
    @abstractmethod
    def accept(self, visitor: 'JsonNodeVisitor'):
        pass

# 抽象访问者
class JsonNodeVisitor(ABC):
    @abstractmethod
    def visit(self, json_node: JsonNode):
        pass


# Json 叶子节点
class JsonLeaf(JsonNode):
    def __init__(self, name, level, _value: Union[str, None]):
        super().__init__(name, level)
        self.value = _value

    def is_leaf(self):
        return True

    def dfs(self, fn: Callable[['JsonNode'], None]):
        fn(self)

    def get_value(self) -> Union[str, None]:
        return self.value

    def accept(self, visitor: 'JsonNodeVisitor'):
        visitor.visit(self)

# Json 组件节点
# 迭代者模式
class JsonComposite(JsonNode):
    def __init__(self, name, level):
        super().__init__(name, level)
        self._children: List[JsonNode] = []

    def add_child(self, node):
        self._children.append(node)

    def remove_child(self, node):
        self._children.remove(node)

    def is_leaf(self):
        return False

    def get_children(self):
        return self._children

    def dfs(self, fn: Callable[['JsonNode'], None]):
        fn(self)
        for child in self._children:
            child.dfs(fn)

    # 迭代器
    def __iter__(self):
        return iter(self._children)

    # 依托于__iter__方法的 accept 
    def accept(self, visitor: 'JsonNodeVisitor'):
        visitor.visit(self)
        
        # 使用 iter 方法之间遍历所有孩子孩子节点进行 accept
        # for child in self:
        #     child.accept(visitor)

class JsonNodeFactory:
    def __init__(self, file_path):
        self.file_path = file_path
        self.parse_json() # 解析 json 文件

    def parse_json(self):
        if os.path.isfile(self.file_path) == False:
            raise FileException(f'File {self.file_path} is not exist')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.json_data = json.load(file) # 第2个属性：json 文件的数据
        if not isinstance(self.json_data, (dict, list)):
            raise FileException(f'JsonNode root must be dict or list')

    # 创建节点
    def create(self) -> JsonNode:
        return self._create_node('', 0, self.json_data)

    def _create_node(self, name: str, level: int, data):
        if isinstance(data, dict): # 根据字典创建节点
            composite = JsonComposite(name, level=level)
            for key, value in data.items():
                child_node = self._create_node(key, level + 1, value)
                composite.add_child(child_node)
            return composite
        elif isinstance(data, list): # 根据列表创建节点
            composite = JsonComposite(name, level=level)
            for idx, item in enumerate(data):
                child_node = self._create_node(f'Array[{idx}]', level + 1, item)
                composite.add_child(child_node)
            return composite
        else:
            return JsonLeaf(name, level, data)
    
    # 创建叶子节点
    def create_leaf(self, name, level, data) -> JsonLeaf:
        if data is None:
            return JsonLeaf(name, level, None)
        else:
            return JsonLeaf(name, level, str(data))





# 用于寻找节点树的 first node 和 last node
class Finder_fist_or_last_Node:
    def __init__(self, json_node: JsonNode):
        self.first = False
        self.first_id = 0   # 第一个 node 的 id
        self.last_id = 0    # 最后一个node 的 id
        json_node.dfs(lambda node: self.finder(node))

    # 判断节点是不是 first node
    def is_first(self, node: JsonNode):
        return node.get_id() == self.first_id
    
    # 判断节点是不是 last node
    def is_last(self, node: JsonNode):
        return node.get_id() == self.last_id

    def finder(self, node: JsonNode):
        if node.is_root(): # 如果node为根节点，则返回
            return
        if not self.first: # 如果还没找到 first node 则进入
            self.first = True
            self.first_id = node.get_id()
        else: # 找到了 first node，则在后面的遍历中不断更新 last_id 就可以找到 the last node
            self.last_id = node.get_id()
