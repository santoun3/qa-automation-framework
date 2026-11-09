from playwright.sync_api import Locator, Page


def _slug(product_name: str) -> str:
    return product_name.lower().replace(" ", "-")


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator('[data-test="error"]')

    def open(self) -> "LoginPage":
        self.page.goto("/")  # base_url comes from config/settings.py via conftest
        return self

    def login(self, username: str, password: str) -> "InventoryPage":
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)


class InventoryPage:
    SORT_OPTIONS = {"name_asc": "az", "name_desc": "za", "price_asc": "lohi", "price_desc": "hilo"}

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator(".product_sort_container")

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        self.page.locator(f'[data-test="add-to-cart-{_slug(product_name)}"]').click()
        return self

    def prices(self) -> list[float]:
        return [float(text.replace("$", "")) for text in self.item_prices.all_inner_texts()]

    def price_of(self, product_name: str) -> float:
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        return float(item.locator(".inventory_item_price").inner_text().replace("$", ""))

    def sort_by(self, option: str) -> "InventoryPage":
        self.sort_dropdown.select_option(self.SORT_OPTIONS[option])
        return self

    def go_to_cart(self) -> "CartPage":
        self.cart_link.click()
        return CartPage(self.page)


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names: Locator = page.locator(".inventory_item_name")
        self.checkout_button = page.locator("#checkout")

    def checkout(self) -> "CheckoutPage":
        self.checkout_button.click()
        return CheckoutPage(self.page)


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.finish_button = page.locator("#finish")
        self.item_total_label = page.locator(".summary_subtotal_label")
        self.confirmation = page.locator(".complete-header")

    def enter_details(self, first: str, last: str, postal_code: str) -> "CheckoutPage":
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal_code)
        self.continue_button.click()
        return self

    def item_total(self) -> float:
        return float(self.item_total_label.inner_text().split("$")[-1])

    def finish(self) -> "CheckoutPage":
        self.finish_button.click()
        return self
