from src.Exception import FileException
from ..icon import IconFamily
from ..node import JsonNodeFactory
from .RectangleStyle import RectangleStyleJsonNodeFactory
from .TreeStyle import TreeStyleJsonNodeFactory

import os
import json

 
class Style_Builder:

    def __init__(self):
        self.icon_family = {
            'default': IconFamily(' ', ' '),
            'poker-face-icon-family': IconFamily('\u2663', '\u2665')
        }
        self.style_factory = {
            'tree': TreeStyleJsonNodeFactory(),
            'rectangle': RectangleStyleJsonNodeFactory()
        }
    
    # 获取当前可以用的 style
    def available_styles(self):
        return list(self.style_factory.keys())
    
    # 获取当前可用的图标族
    def available_icon_family(self):
        return list(self.icon_family.keys())

    # 加载已有的图标集文件
    def load_icon_family(self, file_path):
        if os.path.isfle(file_path) == False:
            raise FileException(f'Error: can not find icon family file: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as file:
            icon_family_dict = json.load(file)
        try:
            for name, _icon_family in icon_family_dict.items():
                self.icon_family[name] = IconFamily(_icon_family["container"], _icon_family["leaf"])
        except KeyError:
            raise FileException(f'Error: icon family file format failed: {file_path}')

    # 创建 Style Json node
    def create_style_node(self, file_path, _icon_family: str, style: str):
        try:
            _icon_family = self.icon_family[_icon_family]
        except KeyError:
            raise FileException(f'Error: can not find icon family file: {file_path}')

        try:
            _style_factory = self.style_factory[style]
        except KeyError:
            raise FileException(f'Error: can not find style: {style}')

        json_node = JsonNodeFactory(file_path).create()
        return _style_factory.create_style_json_node(json_node, _icon_family)
