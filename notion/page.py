
from typing import Any

import json

from notion.client import Client


class Page:

    def __init__(self, id = None, client=None, offline=True, **kwargs) -> None: ## TODO use internal dict
        self.id = id
        self.properties = kwargs
        self.client = client
        self.property_map = {key: type(value) for key, value in self.properties.items()}

        if not offline:
            self.populate()

    def __getattr__(self, __name: str) -> Any:
        return self.properties[__name]
    
    def __repr__(self) -> str:
        return f'Page({", ".join(f'{name}: {repr(prop)}' for name, prop in self.properties.items() if not prop is None)})'    
    
    def populate(self):
        data = self.client.read_page(self.id)
        print(json.dumps(data))
        
    def get_children(self):
        data = self.client.read_hierarchy(self.id)
        print(json.dumps(data))


