from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT = (By.ID, "checkout")

    def item_names(self) -> list[str]:
        if not self.is_present(self.ITEM_NAMES):
            return []
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def checkout(self):
        self.click(self.CHECKOUT)
        from pages.checkout_page import CheckoutPage

        return CheckoutPage(self.driver)
