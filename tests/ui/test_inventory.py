import pytest

pytestmark = pytest.mark.ui


@pytest.mark.regression
def test_catalog_lists_six_products(inventory):
    assert len(inventory.item_names()) == 6


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, key, reverse",
    [
        ("name_asc", "names", False),
        ("name_desc", "names", True),
        ("price_asc", "prices", False),
        ("price_desc", "prices", True),
    ],
)
def test_sorting_orders_products_correctly(inventory, option, key, reverse):
    inventory.sort_by(option)
    values = inventory.item_names() if key == "names" else inventory.item_prices()
    assert values == sorted(values, reverse=reverse)


@pytest.mark.smoke
def test_cart_badge_tracks_added_and_removed_items(inventory):
    assert inventory.cart_count() == 0

    inventory.add_to_cart("Sauce Labs Backpack").add_to_cart("Sauce Labs Bike Light")
    assert inventory.cart_count() == 2

    inventory.remove_from_cart("Sauce Labs Backpack")
    assert inventory.cart_count() == 1
