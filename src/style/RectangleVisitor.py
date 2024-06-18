from ..node import *
from ..icon import IconFamily

class RectangleRenderVisitor(JsonNodeVisitor):
    def __init__(self, icon_family: 'IconFamily', grid_width: int, finder_first_last: 'Finder_fist_or_last_Node'):
        self.icon_family = icon_family
        self.grid_width = grid_width
        self.finder_first_last = finder_first_last

    def visit(self, node: JsonNode):
        if node.is_root():
            return
        line = ''
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

        if node.is_leaf():
            line += self.icon_family.leaf_icon
        else:
            line += self.icon_family.container_icon

        line += node.get_name()

        if node.is_leaf() and node.get_value() is not None:
            line += f': {node.get_value()}'

        line = f'{line} '.ljust(self.grid_width - 2, '─')

        if self.finder_first_last.is_first(node):
            line += '─┐'
        elif self.finder_first_last.is_last(node):
            line += '─┘'
        else:
            line += '─┤'
        print(line)