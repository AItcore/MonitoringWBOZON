from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_stealth import stealth
import time
import re


class WBOZON:

    def __init__(self, WBCards, OZONCards):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.WBCards = WBCards
        self.OZONCards = OZONCards
        self.cardsPlaceWB = {}
        self.cardsPlaceOZON = {}

        self.cardsPlaceByTime = {}

        stealth(
            self.driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True,
        )
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      """},
        )
        self.driver.implicitly_wait(time_to_wait=30)

    def extract_ozon_product_id(self, url: str) -> str | None:
        match = re.search(r"/product/.+?-(\d+)(?:/|\?|$)", url)
        return match.group(1) if match else None

    def setURL(self, url, isWB=False, SearchText=""):
        self.driver.get(url)
        time.sleep(5)
        body = self.driver.find_element(By.TAG_NAME, "body")
        productsOrder = {}
        if isWB:
            for i in range(5):
                body.send_keys(Keys.END)
                time.sleep(2)
        else:
            for i in range(10):
                elements = self.driver.find_elements(By.CLASS_NAME, "tile-root")
                for item in elements:
                    data_order_number = 0
                    try:
                        data_order_number = int(
                            (
                                int(
                                    item.find_element(
                                        By.XPATH, "../../../.."
                                    ).get_attribute("data-index")
                                )
                                + 1
                            )
                            / 2
                        )
                    except:
                        data_order_number = 0
                    try:
                        productsOrder[
                            (int(item.get_attribute("data-index")) + 1)
                            + data_order_number * 8
                        ] = item.find_element(
                            By.CLASS_NAME, "tile-clickable-element"
                        ).get_attribute(
                            "href"
                        )
                    except:
                        pass
                body.send_keys(Keys.END)
                time.sleep(2)
            try:
                elements = self.driver.find_elements(By.CLASS_NAME, "tile-root")
                for item in elements:
                    test = item.find_element(By.XPATH, "../../../..").get_attribute(
                        "data-index"
                    )
                    if not (test is None):
                        productsOrder[
                            (int(item.get_attribute("data-index")) + 1)
                            + (
                                int(
                                    item.find_element(
                                        By.XPATH, "../../../.."
                                    ).get_attribute("data-index")
                                )
                                + 1
                            )
                            / 2
                            * 8
                        ] = item.find_element(
                            By.CLASS_NAME, "tile-clickable-element"
                        ).get_attribute(
                            "href"
                        )
            except:
                pass
        if isWB:
            productsOrder = self.driver.find_element(
                By.CLASS_NAME, "product-card-list"
            ).find_elements(By.TAG_NAME, "article")
            for i, element in enumerate(productsOrder):
                for item in self.WBCards:
                    if item["nmID"] == int(element.get_attribute("data-nm-id")):
                        self.cardsPlaceWB[item["vendorCode"]] = {
                            "searchText": SearchText,
                            "place": i + 1,
                        }

        else:
            for key, element in productsOrder.items():
                for item in self.OZONCards:
                    if item["sku"] == int(self.extract_ozon_product_id(element)):
                        self.cardsPlaceOZON[item["offer_id"]] = {
                            "searchText": SearchText,
                            "place": i + 1,
                        }
