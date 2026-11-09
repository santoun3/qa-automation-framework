from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = BasePage.data_test("error")

    def login(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        # Imported here to avoid a circular import between page modules.
        from pages.inventory_page import InventoryPage

        return InventoryPage(self.driver)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)
