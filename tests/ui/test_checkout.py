import pytest

from test_data.factories import CHECKOUT_CUSTOMER

pytestmark = pytest.mark.ui

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]


@pytest.mark.smoke
def test_customer_can_complete_a_purchase(inventory):
    """End-to-end critical path: browse, add to cart, check out, confirm the order."""
    prices = dict(zip(inventory.item_names(), inventory.item_prices(), strict=True))
    for product in PRODUCTS:
        inventory.add_to_cart(product)

    cart = inventory.go_to_cart()
    assert sorted(cart.item_names()) == sorted(PRODUCTS)

    checkout = cart.checkout().enter_details(**CHECKOUT_CUSTOMER)
    # The order summary must charge exactly what the catalog advertised.
    assert checkout.item_total() == pytest.approx(sum(prices[p] for p in PRODUCTS))

    checkout.finish()
    assert checkout.confirmation() == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal_code, expected_error",
    [
        ("", "Customer", "67202", "First Name is required"),
        ("Test", "", "67202", "Last Name is required"),
        ("Test", "Customer", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_requires_customer_details(inventory, first, last, postal_code, expected_error):
    inventory.add_to_cart(PRODUCTS[0])
    checkout = inventory.go_to_cart().checkout().enter_details(first, last, postal_code)
    assert expected_error in checkout.error_message()
