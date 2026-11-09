"""Shared behavior for every page object.

Tests never touch raw locators or WebDriver calls. They call intent-level methods on
page objects, so a UI change means updating one locator here, not fifty tests."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings

Locator = tuple[str, str]


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT_SECONDS)

    def open(self):
        self.driver.get(settings.UI_BASE_URL + self.path)
        return self

    # Explicit waits only: no time.sleep anywhere in the framework.
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str) -> None:
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def is_present(self, locator: Locator) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    @staticmethod
    def data_test(value: str) -> Locator:
        """Sauce Demo exposes stable data-test attributes; prefer them over CSS classes."""
        return (By.CSS_SELECTOR, f'[data-test="{value}"]')
