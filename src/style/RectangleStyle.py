from .style import StyleJsonNode, StyleJsonNodeFactory
from ..node import *
from ..icon import IconFamily
from .RectangleVisitor import RectangleRenderVisitor

class RectangleStyledJSONNode(StyleJsonNode):
    def __init__(self, root: JsonNode, icon_family: IconFamily):
        super().__init__(root, icon_family)
        self.grid_width = 16
        self.json_node.dfs(lambda node: self.update_grid_width(node))
        self.finder_first_last = Finder_fist_or_last_Node(root)

    def update_grid_width(self, node: JsonNode):
        notation_length = max((node.get_level() - 1) * 3 + 2, 0)
        name_length = len(node.get_name()) + 2
        if node.is_leaf() and node.get_value() is not None:
            name_length += len(str(node.get_value())) + 2
        self.grid_width = max(self.grid_width, notation_length + name_length + 2)
   
    def accept(self, method="iterator_visitor") -> None:
        if method == "dfs": # 使用 dfs 方法遍历
            self.json_node.dfs(lambda node: self.render(node))
        elif method == "iterator_visitor": # 使用迭代器 + 访问者模式方法
            visitor = RectangleRenderVisitor(self.icon_family, self.grid_width, self.finder_first_last)
            for node in self.iterate_nodes(self.json_node):
                node.accept(visitor)
            # self.json_node.accept(visitor)

    # 遍历节点
    def iterate_nodes(self, node: JsonNode):
        yield node
        if not node.is_leaf():
            for child in node:
                yield from self.iterate_nodes(child)

    def render(self, node: JsonNode):
        if node.is_root(): 
            return
        line = ''
        # 第一层
        if self.finder_first_last.is_first(node):
            line += "┌─"
        elif self.finder_first_last.is_last(node):
            line += "└─"
        elif node.get_level() == 1:
            line += "├─"
        else:
            line += "│ "

        if node.get_level() > 2:
            if self.finder_first_last.is_last(node):
                line += '─┴─' * (node.get_level() - 2)
            else:
                line += ' │ ' * (node.get_level() - 2)

        if self.finder_first_last.is_last(node):
            line += '─┴─'
        elif node.get_level() > 1:
            line += ' ├─'
        
        # 图标
        if node.is_leaf():
            line += self.icon_family.leaf_icon
        else:
            line += self.icon_family.container_icon
        # 名字
        line += node.get_name()
        # 值
        if node.is_leaf() and node.get_value() is not None:
            line += f': {node.get_value()}'
        # padding
        line = f'{line} '.ljust(self.grid_width - 2, '─')
        # 最后一层
        if self.finder_first_last.is_first(node):
            line += '─┐'
        elif self.finder_first_last.is_last(node):
            line += '─┘'
        else:
            line += '─┤'
        print(line)


class RectangleStyleJsonNodeFactory(StyleJsonNodeFactory):
    def create_style_json_node(self, json_node: JsonNode, icon_family: IconFamily) -> StyleJsonNode:
        return RectangleStyledJSONNode(json_node, icon_family)

