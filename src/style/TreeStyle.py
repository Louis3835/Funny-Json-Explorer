from .style import StyleJsonNode, StyleJsonNodeFactory
from ..node import *
from ..icon import IconFamily
from .TreeVisitor import TreeRenderVisitor

 
class TreeStyleJsonNode(StyleJsonNode):
    def __init__(self, root: JsonNode, icon_family: IconFamily):
        super().__init__(root, icon_family)

    # 渲染全部
    def accept(self, method = "iterator_visitor"):
        if method == "origin":
            self.render_container('', '', self.json_node)
        elif method == "iterator_visitor": # 使用访问者模式方法
            visitor = TreeRenderVisitor(self.icon_family)
            self.json_node.accept(visitor)

    # 根据节点类型选择渲染方法
    def render(self, notation_first, notation_second, node: JsonNode):
        if node.is_leaf():
            self.render_leaf(notation_first, node)
        else:
            self.render_container(notation_first, notation_second, node)

    def render_leaf(self, notation: str, node: JsonNode):
        value = node.get_value() # 获取节点的值
        if value is None: # 如果节点为空，则不打印值
            print(f'{notation}{self.icon_family.leaf_icon}{node.get_name()}')
        else:
            print(f'{notation}{self.icon_family.leaf_icon}{node.get_name()}: {value}')

    def render_container(self, notation_first, notation_second, node: JsonNode):
        if not node.is_root(): # 如果不为根节点
            print(f'{notation_first}{self.icon_family.container_icon}{node.get_name()}')
        
        children = node.get_children()
        if(len(children) == 0):
            return
        for child in children[:-1]: # 对于第一个到倒数第二个孩子节点
            self.render(f'{notation_second}├─', f'{notation_second}│    ', child)

        # 对于最后一个孩子节点
        self.render(f'{notation_second}└─', f'{notation_second}     ', children[-1])


# 工厂用于创建 Style node
class TreeStyleJsonNodeFactory(StyleJsonNodeFactory):
    
    def create_style_json_node(self, json_node: JsonNode, icon_family: IconFamily) -> StyleJsonNode:
        return TreeStyleJsonNode(json_node, icon_family)