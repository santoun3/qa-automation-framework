"""Playwright fixtures. pytest-playwright supplies `page` (a fresh, isolated browser
context per test); this file points it at the app and logs in for tests that need it."""

import pytest
from playwright.sync_api import Page

from config import settings
from pw_pages import InventoryPage, LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": settings.UI_BASE_URL,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory(login_page: LoginPage) -> InventoryPage:
    return login_page.login(settings.STANDARD_USER, settings.UI_PASSWORD)
