import asyncio
from pprint import pprint
from datetime import datetime

from Selenium.driver import WBOZON
from API.WB.Cards import WB_API
from API.OZON.Cards import OZON_API
from Database.DAO.DAO import PlaceHistoryDAO

from urllib.parse import quote


def record_cards(cards):
    pass

def filter_best_places(records: list[dict]) -> list[dict]:
    """
    Оставляет по одной записи на каждую пару (marketplace, search_text)
    с минимальным значением place.
    """
    best: dict[tuple[str, str], dict] = {}

    for rec in records:
        key = (rec["marketplace"], rec["search_text"])
        current = best.get(key)

        if current is None or rec["place"] < current["place"]:
            best[key] = rec

    return list(best.values())

async def record_place(cardsPlaceByTime):
    data_to_save = []
    for time, marketplace in cardsPlaceByTime.items():
        for key, item in marketplace.items():
            for vendor_code, info in item.items():
                data_to_save.append(
                    {
                        "date_time_check": datetime.strptime(time,"%d.%m.%Y %H:%M"),
                        "marketplace": key,
                        "vendor_code": vendor_code,
                        "place": info["place"],
                        "search_text": info["searchText"],
                    }
                )
    data_to_save = filter_best_places(data_to_save)
    await PlaceHistoryDAO.bulk_create(data_to_save)

async def main():
    WBCards = WB_API.GetAllCards()
    OZONCards = OZON_API.GetAllCards()
    driver = WBOZON(WBCards, OZONCards)
    while True:
        driver.setURL(
            f"https://www.wildberries.ru/catalog/0/search.aspx?search={quote("Протеин")}",
            True,
            "Протеин",
        )
        driver.setURL(
            f"https://www.wildberries.ru/catalog/0/search.aspx?search={quote("Креатин")}",
            True,
            "Креатин",
        )
        driver.setURL(
            f"https://www.ozon.ru/category/proteiny-11675/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={quote("Протеин")}",
            SearchText="Протеин",
        )
        driver.setURL(
            f"https://www.ozon.ru/category/kreatiny-11667/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={quote("Креатин")}",
            SearchText="Креатин",
        )

        time = datetime.now().strftime("%d.%m.%Y %H:%M")

        driver.cardsPlaceByTime = {
            time: {"WB": driver.cardsPlaceWB, "OZON": driver.cardsPlaceOZON}
        }

        driver.cardsPlaceWB = {}
        driver.cardsPlaceOZON = {}
        await record_place(driver.cardsPlaceByTime)

if __name__ == "__main__":
    asyncio.run(main())
