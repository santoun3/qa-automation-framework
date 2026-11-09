"""Playwright page objects for Sauce Demo.

Same Page Object Model as the Selenium suite in pages/, built on Playwright's API:
locators re-resolve on every use and actions wait automatically, so there are no
explicit waits here at all."""

from pw_pages.sauce_demo import CartPage, CheckoutPage, InventoryPage, LoginPage

__all__ = ["CartPage", "CheckoutPage", "InventoryPage", "LoginPage"]
