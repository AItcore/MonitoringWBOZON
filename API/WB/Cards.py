import requests
import os

WB_TOKEN = os.getenv("API_WB_TOKEN")

class WB_API:
    def GetAllCards():
        url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
        headers = {"Authorization": WB_TOKEN, "Accept": "application/json"}
        data = {
            "settings": {
                "sort": {"ascending": True},
                "cursor": {"limit": 100},
                "filter": {"withPhoto": -1},
            }
        }
        return requests.post(url=url, json=data, headers=headers).json()['cards']
