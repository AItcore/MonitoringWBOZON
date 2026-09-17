from Selenium.driver import WBOZON
from API.WB.Cards import WB_API
from API.OZON.Cards import OZON_API


if __name__ == "__main__":
    WBCards = WB_API.GetAllCards()
    OZONCards = OZON_API.GetAllCards()
    driver = WBOZON(WBCards, OZONCards)
    while True:
        # driver.setURL("https://www.wildberries.by/catalog/0/search.aspx?search=%D0%9F%D1%80%D0%BE%D1%82%D0%B5%D0%B8%D0%BD", True)
        driver.setURL("https://www.ozon.ru/category/proteiny-11675/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D0%BF%D1%80%D0%BE%D1%82%D0%B5%D0%B8%D0%BD")
    