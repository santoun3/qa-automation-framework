from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = BasePage.data_test("error")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def enter_details(self, first: str, last: str, postal_code: str) -> "CheckoutPage":
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)
        return self

    def item_total(self) -> float:
        # Label reads like "Item total: $39.98"
        return float(self.text_of(self.ITEM_TOTAL).split("$")[-1])

    def finish(self) -> "CheckoutPage":
        self.click(self.FINISH)
        return self

    def confirmation(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)
