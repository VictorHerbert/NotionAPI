from typing import Any, Dict

import json

from notion.client import Client


class Block:

    def __init__(self, client, id = None, **kwargs) -> None: ## TODO use internal dict
        self.id = id
        self.properties = kwargs
        self.client = client
        self.property_map = {key: type(value) for key, value in self.properties.items()}        

    def __getattr__(self, __name: str) -> Any:
        return self.properties[__name]
    
    def __repr__(self) -> str:
        return f'Block({", ".join(f'{name}: {repr(prop)}' for name, prop in self.properties.items() if not prop is None)})'    
        
        
    def get_children(self):
        data = self.client.read_hierarchy(self.id)
        print(json.dumps(data))


class Mermaid(Block):
    
    class Theme:
        DEFAULT = 'default'
        NEUTRAL = 'neutral'
        DARK =  'dark'
        FOREST = 'forest'
        BASE = 'base'

    def __init__(self, client=None, id=None, theme=Theme.FOREST, **kwargs) -> None:
        super().__init__(client, id, **kwargs)

        self.theme= "%%{init: {'theme':'" + theme + "'}}%%"
    
    def update_code(self, code):
        self.client.update_block(self.id, {
            "code": {
                "rich_text": [
                        {
                            "text": {
                                "content": code,
                            }
                        }
                    ]
                }
            }
        )

class MermaidLineChart(Mermaid):

    def __init__(self, client, id=None, title=None, x_axis = None, **kwargs) -> None:
        super().__init__(client, id, **kwargs)

        self.title = title
        if not x_axis is None:
            self.set_x_axis(x_axis)
        self.y_list = ''
        
    def set_x_axis(self, x_axis: list[str|float]) -> None:
        self.x_axis = f'x-axis [{",".join(str(col) for col in x_axis)}]\n'

    def clear_data(self) -> None:
        self.y_list = ''

    def insert_line(self, data: list[float]) -> None:
        self.y_list += f'line [{",".join(str(point) for point in data)}]\n'

    def insert_line(self, data: list[float]) -> None:
        self.y_list += f'line [{",".join(str(point) for point in data)}]\n'

    def generate_code(self):
        code = self.theme
        code += 'xychart-beta\n'
        if not self.title is None:
            code += self.title
        code += self.x_axis
        code += self.y_list
        
    def update(self):
        self.generate_code


class MermaidPieChart(Mermaid):

    def __init__(self, client, id=None, data : Dict[str, float] = None, title=None, theme=Mermaid.Theme.DEFAULT, show_data = True, **kwargs) -> None:
        super().__init__(client, id, theme, **kwargs)

        self.title = title
        self.data = data
        self.show_data = show_data
        
    def get_code(self):
        code = self.theme + '\n'
        code += 'pie' + (' showData' if self.show_data else '') + '\n'
        if not self.title is None:
            code += 'title ' + self.title + '\n'
        
        for key, value in self.data.items():
            code += f'"{key}" : {value}\n'

        return code

        
    def update(self):
        self.update_code(self.get_code())

