import pytest
from playwright.sync_api import expect

from test_data.factories import CHECKOUT_CUSTOMER

pytestmark = pytest.mark.playwright

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]


@pytest.mark.smoke
def test_customer_can_complete_a_purchase(inventory):
    """Same critical path as the Selenium suite, written with Playwright."""
    expected_total = sum(inventory.price_of(p) for p in PRODUCTS)
    for product in PRODUCTS:
        inventory.add_to_cart(product)
    expect(inventory.cart_badge).to_have_text(str(len(PRODUCTS)))

    cart = inventory.go_to_cart()
    expect(cart.item_names).to_have_text(PRODUCTS, use_inner_text=True)

    checkout = cart.checkout().enter_details(**CHECKOUT_CUSTOMER)
    assert checkout.item_total() == pytest.approx(expected_total)

    checkout.finish()
    expect(checkout.confirmation).to_have_text("Thank you for your order!")
