"""Shared pytest fixtures and hooks.

- driver: a fresh, isolated browser per test (headless in CI)
- On any UI test failure, a screenshot is saved and embedded in the HTML report
- API fixtures create their own data and clean it up afterwards
"""

from pathlib import Path

import pytest
from selenium import webdriver

from api_client import BookingClient
from config import settings
from pages import InventoryPage, LoginPage
from test_data.factories import booking_payload

SCREENSHOT_DIR = Path("reports/screenshots")


# ---------------------------------------------------------------- UI fixtures
def _build_driver():
    if settings.BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        if settings.HEADLESS:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
    else:
        options = webdriver.ChromeOptions()
        if settings.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,900")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Sauce Demo can trigger Chrome's password-breach popup, which blocks clicks.
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        driver = webdriver.Chrome(options=options)  # Selenium Manager resolves the driver
    driver.implicitly_wait(0)  # explicit waits only, so timing is predictable
    return driver


@pytest.fixture
def driver():
    drv = _build_driver()
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver).open()


@pytest.fixture
def inventory(login_page) -> InventoryPage:
    page = login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)
    assert page.is_loaded(), "Precondition failed: could not log in as the standard user"
    return page


# --------------------------------------------------------------- API fixtures
@pytest.fixture
def api() -> BookingClient:
    return BookingClient()


@pytest.fixture
def authed_api() -> BookingClient:
    client = BookingClient()
    client.authenticate()
    return client


@pytest.fixture
def booking(authed_api):
    """Creates a booking for the test and deletes it afterwards, pass or fail."""
    payload = booking_payload()
    response = authed_api.create_booking(payload)
    assert response.status_code == 200, f"Setup failed: {response.status_code} {response.text}"
    booking_id = response.json()["bookingid"]
    yield booking_id, payload
    authed_api.delete_booking(booking_id)


# ---------------------------------------------- Screenshot on failure (UI only)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOT_DIR / f"{item.name}.png"
    drv.save_screenshot(str(path))

    html_plugin = item.config.pluginmanager.getplugin("html")
    if html_plugin is not None:
        extras = getattr(report, "extras", [])
        extras.append(
            html_plugin.extras.image(drv.get_screenshot_as_base64(), "Failure screenshot")
        )
        extras.append(html_plugin.extras.url(drv.current_url, "Page at failure"))
        report.extras = extras
