"""Central configuration. Every value can be overridden with an environment variable,
so the same suite runs locally, in CI, or against another environment without code changes."""

import os

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")

# Sauce Demo publishes these demo accounts on its login page.
STANDARD_USER = os.getenv("UI_USER", "standard_user")
LOCKED_OUT_USER = "locked_out_user"
UI_PASSWORD = os.getenv("UI_PASSWORD", "secret_sauce")

# Restful Booker's documented demo admin account.
API_ADMIN_USER = os.getenv("API_USER", "admin")
API_ADMIN_PASSWORD = os.getenv("API_PASSWORD", "password123")

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome").lower()
EXPLICIT_WAIT_SECONDS = int(os.getenv("EXPLICIT_WAIT_SECONDS", "10"))
API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "15"))
