import requests, json
import pandas as pd

from .property import Property
from .page import Page
from .client import Client

class Database:

    def __init__(self, client: Client, databaseID: str, populate = False) -> None:
        self.client = client
        self.databaseID = databaseID ## TODO use regex to allow url
        self.pages = []
        self.property_map = {}
        if populate:
            self.populate()

    def __repr__(self) -> str:
        return f'Database({"".join("\n\t" + repr(page) for page in self.pages)})'

    def populate(self):
        json_response = self.client.readDatabaseRaw(self.databaseID)

        for page in json_response['results']:
            properties = {name : Property.from_json(name, property_json) for name, property_json in page['properties'].items()}
            new_page = Page(id=page['id'], **properties)
            self.pages.append(new_page)
            self.property_map = {**self.property_map, **new_page.property_map}

    def validate_page(self, page: Page) -> bool:
        for key, value in page.property_map.items():
            if self.property_map[key] != value:
                return False
        return True

    def createPage(self, page: Page) -> None:
        if not self.validate_page(page):
            raise TypeError('Page properties do not match Database')

        page_json = {
            "parent": { "database_id": self.databaseID },
            "properties": {
                key : prop.to_json() for key, prop in page.properties.items()
            }
        }

        self.client.createPage(json.dumps(page_json))

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([{prop: value.to_pandas_dtype() for prop, value in page.properties.items() if not value is None} for page in self.pages])
