from typing import ClassVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    SORT_OPTIONS: ClassVar[dict[str, str]] = {
        "name_asc": "az",
        "name_desc": "za",
        "price_asc": "lohi",
        "price_desc": "hilo",
    }

    def is_loaded(self) -> bool:
        return (
            "inventory.html" in self.driver.current_url and self.text_of(self.TITLE) == "Products"
        )

    def item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def item_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICES)]

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        slug = product_name.lower().replace(" ", "-")
        self.click(self.data_test(f"add-to-cart-{slug}"))
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        slug = product_name.lower().replace(" ", "-")
        self.click(self.data_test(f"remove-{slug}"))
        return self

    def cart_count(self) -> int:
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def sort_by(self, option: str) -> "InventoryPage":
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(self.SORT_OPTIONS[option])
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage

        return CartPage(self.driver)
