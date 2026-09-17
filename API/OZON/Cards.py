import requests
import os

OZON_CLIENT = os.getenv("API_OZON_CLIENT")
OZON_TOKEN = os.getenv("API_OZON_TOKEN")


class OZON_API:
    def GetAllCards():
        url = "https://content-api.wildberries.ru/content/v2/get/cards/list"
        headers = {"Client-Id": OZON_CLIENT,"Api-Key":OZON_TOKEN , "Accept": "application/json"}
        data = {
            "limit": 1000
        }
        return requests.post(url=url, json=data, headers=headers).json()['result']['items']
