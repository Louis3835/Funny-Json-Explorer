from ..node import *
from ..icon import IconFamily

class TreeRenderVisitor(JsonNodeVisitor):
    def __init__(self, icon_family: 'IconFamily'):
        self.icon_family = icon_family
        self.notation_stack = [("", "")]

    def visit(self, node: 'JsonNode'):
        if node.is_leaf():
            self.render_leaf(node)
        else:
            self.render_container(node)

    def render_leaf(self, node: JsonNode):
        notation, _ = self.notation_stack[-1]
        value = node.get_value()
        if value is None:
            print(f'{notation}{self.icon_family.leaf_icon}{node.get_name()}')
        else:
            print(f'{notation}{self.icon_family.leaf_icon}{node.get_name()}: {value}')

    def render_container(self, node: JsonNode):
        notation_first, notation_second = self.notation_stack[-1]
        if not node.is_root():
            print(f'{notation_first}{self.icon_family.container_icon}{node.get_name()}')
        children = node.get_children()
        if not children:
            return
        for child in children[:-1]: 
            self.notation_stack.append((f'{notation_second}├─', f'{notation_second}│    '))
            child.accept(self) # 调用 JsonNode accept
            self.notation_stack.pop()
        self.notation_stack.append((f'{notation_second}└─', f'{notation_second}     '))
        children[-1].accept(self)
        self.notation_stack.pop()