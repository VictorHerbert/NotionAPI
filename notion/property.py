from datetime import datetime
import json

class Property:
    TYPES = {}
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def from_json(name, json):
        property_type = json['type']
        if not json[property_type] is None and json[property_type] != []:
            return Property.TYPES[property_type].from_json(name, json[property_type])
        else:
            return None
        
    def to_json(self) -> json:
        return NotImplementedError()
        
    def to_pandas_dtype(self):
        return self

        
class Date(Property):

    def __init__(self, start = None, end = None) -> None: ## TODO timezone
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f'Date({self.start}->{self.end})'

    def from_json(name, json):
        start, end = None, None

        if not json['start'] is None:
            start = datetime.strptime(json['start'], '%Y-%m-%d')
        if not json['end'] is None:
            end = datetime.strptime(json['end'], '%Y-%m-%d')
        
        return Date(start, end)
    
    def to_json(self) -> json:
        return {
            "date": {
                "start": self.start.strftime("%Y-%m-%d")
            }
        }
    
    def to_pandas_dtype(self):
        return self.start
    

class Tags(Property):
    
    def __init__(self, tags) -> None:
        self.tags = tags

    def __repr__(self) -> str:
        return f'Tags[{",".join(self.tags)}]'

    def from_json(name, json):
        if json != []:
            return Tags([tag['name'] for tag in json])
        
    def to_pandas_dtype(self):
        return [tag for tag in self.tags]

class Title(Property):
    
    def __init__(self, title) -> None:
        self.title = title

    def __repr__(self) -> str:
        return self.title

    def from_json(name, json):
        return Title(json[0]['plain_text']) #TODO its only getting the first block of title
    
    def to_json(self) -> json:
        return {
            "title": [
                {
                    "text": {
                        "content": self.title
                    }
                }
            ]
        }

class Checkbox(Property):

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'Checkbox({self.value})'

    def from_json(name, json):
        return Checkbox(json)

    def to_json(self):
        return {"checkbox" : self.value}
    
            
    def to_pandas_dtype(self):
        return self.value


class Number(Property):

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'Number({self.value})'

    def from_json(name, json):
        return Number(json)

    def to_json(self):
        return {"number" : self.value}
    
            
    def to_pandas_dtype(self):
        return self.value

Property.TYPES = {
    'date' : Date,
    'multi_select' : Tags,
    'title' : Title,
    'checkbox' : Checkbox,
    'number' : Number
}