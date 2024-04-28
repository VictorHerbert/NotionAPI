#TODO make requests using an external client
import requests, json
from diskcache import Cache

#FIXME
cache = Cache("cachedir")


class ClientBase:

    def get(self, url):
        res = requests.request("GET", url, headers=self.headers)
        return res.json(), res.status_code
    
    def post(self, url, data) -> int:
        res = requests.request("POST", url, headers=self.headers, data=data)
        return res.status_code

class Client(ClientBase):

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

    #@cache.memoize()
    def readDatabaseRaw(self, databaseID) -> json:
        print('Calling API...')
        readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
        res = requests.request("POST", readUrl, headers=self.headers)
        data = res.json()

        with open('data.json', 'w') as f:
            json.dump(data, f)

        return data

    PAGE_URL = 'https://api.notion.com/v1/pages/'
    BLOCK_URL = 'https://api.notion.com/v1/blocks/'

    def read_page(self, id: str) -> json:
        data, code = self.get(Client.PAGE_URL + id)
        return data

    def createPage(self, data: json) -> int:
        return self.post(Client.PAGE_URL, data)
    
    def read_hierarchy(self, id: str) -> json:
        data, code = self.get(Client.BLOCK_URL + id + '/children')
        return data

    def update_block(self, block_id, data):
        url = f"https://api.notion.com/v1/blocks/{block_id}"
        data = json.dumps(data)
        res = requests.request("PATCH", url, headers=self.headers, data=data)
        return res.status_code