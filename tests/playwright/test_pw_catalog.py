import pytest
from playwright.sync_api import Route, expect

pytestmark = pytest.mark.playwright


@pytest.mark.regression
def test_price_sort_low_to_high(inventory):
    inventory.sort_by("price_asc")
    prices = inventory.prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_store_still_works_when_product_images_fail(login_page):
    """Network interception: make every product image fail, then confirm a shopper
    can still browse and add to cart. This kind of resilience check is hard to
    write in Selenium and takes a few lines in Playwright."""
    blocked: list[str] = []

    def fail_image(route: Route):
        blocked.append(route.request.url)
        route.abort()

    login_page.page.route("**/*.{jpg,jpeg,png}", fail_image)
    inventory = login_page.login("standard_user", "secret_sauce")

    expect(inventory.item_names).to_have_count(6)
    inventory.add_to_cart("Sauce Labs Backpack")
    expect(inventory.cart_badge).to_have_text("1")
    assert blocked, "Expected product image requests to be intercepted"
