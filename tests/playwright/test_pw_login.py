import re

import pytest
from playwright.sync_api import expect

from config import settings

pytestmark = pytest.mark.playwright


@pytest.mark.smoke
def test_standard_user_can_log_in(login_page):
    inventory = login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)

    # expect() retries until the condition holds or times out: no manual waits.
    expect(inventory.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.title).to_have_text("Products")


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
        ("standard_user", "wrong_password", "Username and password do not match"),
    ],
    ids=["locked-out-user", "wrong-password"],
)
def test_invalid_login_shows_clear_error(login_page, username, password, expected_error):
    login_page.login(username, password)

    expect(login_page.error).to_contain_text(expected_error)
    expect(login_page.page).not_to_have_url(re.compile(r"inventory"))
