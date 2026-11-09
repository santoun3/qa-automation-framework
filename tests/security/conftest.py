"""Fixtures for browser-based security tests (Playwright). API security tests reuse the
`api`, `authed_api` and `booking` fixtures from the root conftest.py."""

import pytest
from playwright.sync_api import Page

from config import settings
from pw_pages import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": settings.UI_BASE_URL,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture
def dialogs(page: Page) -> list[str]:
    """Records any JavaScript alert/confirm/prompt. An XSS payload that executes
    would open one, so security tests assert this list stays empty."""
    fired: list[str] = []

    def _record(dialog):
        fired.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", _record)
    return fired


@pytest.fixture
def sec_login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()
