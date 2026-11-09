"""Browser security checks: protected pages need a session, logout really ends it,
and script injected into form fields never executes."""

import re

import pytest
from playwright.sync_api import expect

from config import settings
from test_data.factories import CHECKOUT_CUSTOMER

pytestmark = pytest.mark.security

XSS_PAYLOAD = "<script>alert('xss')</script>"


@pytest.mark.smoke
@pytest.mark.parametrize("path", ["/inventory.html", "/cart.html"])
def test_protected_pages_require_login(page, path):
    page.goto(path)

    expect(page).not_to_have_url(re.compile(re.escape(path)))
    expect(page.locator('[data-test="error"]')).to_contain_text("when you are logged in")


@pytest.mark.regression
def test_logout_ends_the_session(sec_login_page):
    page = sec_login_page.page
    sec_login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))

    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    expect(page.locator("#login-button")).to_be_visible()

    # Going straight back to a protected page must not restore the old session.
    page.goto("/inventory.html")
    expect(page.locator('[data-test="error"]')).to_contain_text("when you are logged in")


@pytest.mark.regression
def test_script_in_login_fields_does_not_execute(sec_login_page, dialogs):
    sec_login_page.login(XSS_PAYLOAD, XSS_PAYLOAD)

    expect(sec_login_page.error).to_be_visible()
    assert dialogs == [], f"Injected script executed: {dialogs}"


@pytest.mark.regression
def test_script_in_checkout_fields_does_not_execute(sec_login_page, dialogs):
    inventory = sec_login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)
    inventory.add_to_cart("Sauce Labs Backpack")
    checkout = inventory.go_to_cart().checkout()

    checkout.enter_details(XSS_PAYLOAD, XSS_PAYLOAD, CHECKOUT_CUSTOMER["postal_code"]).finish()

    expect(checkout.confirmation).to_have_text("Thank you for your order!")
    assert dialogs == [], f"Injected script executed: {dialogs}"
