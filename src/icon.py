
# 图标模块
class IconFamily:
    def __init__(self, container, leaf):
        self.container_icon = container
        self.leaf_icon = leaf
    
    def get_family(self, node_type):
        if node_type == "container":
            return self.container_icon
        elif node_type == "leaf":
            return self.leaf_icon