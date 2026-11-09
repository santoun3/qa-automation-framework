import pytest

from config import settings

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_standard_user_can_log_in(login_page):
    inventory = login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)
    assert inventory.is_loaded()


# Data-driven negative tests: one test function, many cases, each reported separately.
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked-out-user", "wrong-password", "missing-username", "missing-password"],
)
def test_invalid_login_shows_clear_error(login_page, username, password, expected_error):
    login_page.login(username, password)
    assert expected_error in login_page.error_message()
    assert "inventory" not in login_page.driver.current_url
