# QA Automation Framework — UI + API + Security

[![Tests](https://github.com/santoun3/qa-automation-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/santoun3/qa-automation-framework/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Selenium](https://img.shields.io/badge/selenium-4-43B02A)
![Playwright](https://img.shields.io/badge/playwright-1-2EAD33)
![pytest](https://img.shields.io/badge/pytest-8-0A9EDC)
![OWASP ZAP](https://img.shields.io/badge/OWASP%20ZAP-baseline-00549E)

A test automation framework built the way I build them for production teams: page objects,
independent tests, data-driven cases, contract checks on the API, and a CI pipeline that runs
fast smoke tests on every push and the full regression suite nightly. The UI layer is covered
twice, in **Selenium** and in **Playwright**, so the two approaches can be compared side by side.
A **security layer** checks authentication, authorization and injection handling, and an
**OWASP ZAP** scan runs in the pipeline.

It tests two public practice applications:

- **UI:** [Sauce Demo](https://www.saucedemo.com), an e-commerce site (login, catalog, cart, checkout)
- **API:** [Restful Booker](https://restful-booker.herokuapp.com/apidoc/index.html), a hotel booking REST API (auth, full CRUD)

**Author:** Sherif Antoun · Senior QA Automation Engineer · [LinkedIn](https://www.linkedin.com/in/sherifantoun)

---

## What this demonstrates

| Practice | Where to look |
| --- | --- |
| Page Object Model: tests read like user stories, locators live in one place | `pages/` |
| Explicit waits only, no `sleep()`, for stable, fast UI tests | `pages/base_page.py` |
| Playwright page objects with auto-waiting locators and retrying `expect()` assertions | `pw_pages/`, `tests/playwright/` |
| Network interception: the store still works when product images fail | `tests/playwright/test_pw_catalog.py` |
| Data-driven testing with `pytest.mark.parametrize` | `tests/ui/test_login.py`, `tests/ui/test_checkout.py` |
| End-to-end critical path, including a price-integrity check | `tests/ui/test_checkout.py` |
| API contract testing with JSON Schema | `api_client/schemas.py`, `tests/api/test_bookings.py` |
| Negative and security checks (bad credentials, missing auth token) | `tests/api/test_auth.py` |
| API authorization: no token, forged token and wrong Basic auth are all rejected, and data stays unchanged | `tests/security/test_api_security.py` |
| Injection: SQL-injection-style credentials never earn a token; script in form fields never executes | `tests/security/` |
| Session security: protected pages need login, and logout really ends the session | `tests/security/test_ui_security.py` |
| OWASP ZAP baseline scan in CI, with findings summarized on every run | `.github/workflows/tests.yml` (`zap-baseline` job) |
| Test isolation: every test creates and cleans up its own data | `conftest.py` (`booking` fixture), `test_data/factories.py` |
| Screenshot on any UI failure; Playwright traces kept for failed tests | `conftest.py`, `.github/workflows/tests.yml` |
| Environment-driven config: same suite, any environment | `config/settings.py` |
| CI/CD: four parallel test jobs (API, Selenium, Playwright, Security) plus a ZAP scan, smoke vs. regression scope, HTML + JUnit reports | `.github/workflows/tests.yml` |

## Test coverage

| Area | Tests | Covers |
| --- | --- | --- |
| Selenium · Login | 5 | Valid login, locked-out user, wrong password, missing fields |
| Selenium · Catalog | 6 | Product count, 4 sort orders, cart badge add/remove |
| Selenium · Checkout | 4 | Full purchase with total verification, 3 required-field validations |
| Playwright · Login | 3 | Valid login, locked-out user, wrong password |
| Playwright · Checkout | 1 | Full purchase with cart badge, cart contents and total verification |
| Playwright · Catalog | 2 | Price sort, store still works when product images fail (network interception) |
| API · Auth | 4 | Health check, token issue, bad credentials, update without token (403) |
| API · Bookings | 7 | Create, read, filter, full update, partial update, delete, unknown ID (404) |
| Security · API | 7 | Delete/update without token, forged token, wrong Basic auth, 3 SQL-injection-style logins |
| Security · UI | 5 | 2 protected pages without login, logout ends session, XSS in login and checkout fields |
| **Total** | **44** | Plus an OWASP ZAP baseline scan on every run |

## Project structure

```
├── .github/workflows/tests.yml   # CI: smoke on push/PR, full regression nightly
├── api_client/
│   ├── booking_client.py         # API wrapper: URLs, headers and auth in one place
│   └── schemas.py                # JSON Schemas for contract tests
├── config/settings.py            # All settings overridable by environment variable
├── pages/                        # Selenium page objects (base, login, inventory, cart, checkout)
├── pw_pages/                     # Playwright page objects
├── test_data/factories.py        # Unique test data per run
├── tests/
│   ├── api/                      # REST API tests
│   ├── playwright/               # Playwright browser tests
│   ├── security/                 # API and browser security tests
│   └── ui/                       # Selenium browser tests
├── conftest.py                   # Fixtures, setup/teardown, failure screenshots
└── pytest.ini                    # Markers: ui, playwright, api, security, smoke, regression
```

## Run it locally

Requires Python 3.10+ and Chrome (for Selenium).

```bash
git clone https://github.com/santoun3/qa-automation-framework.git
cd qa-automation-framework
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium                         # browser for the Playwright tests

pytest                         # everything
pytest -m smoke                # fast critical-path checks
pytest -m api                  # API only
pytest -m playwright           # Playwright only
pytest -m security             # security tests only
pytest -m "ui and regression"  # combine markers
pytest -n auto                 # run in parallel
HEADLESS=false pytest -m ui    # watch the Selenium browser
pytest -m playwright --headed  # watch the Playwright browser
pytest --html=reports/report.html --self-contained-html   # HTML report
```

Selenium Manager downloads the matching ChromeDriver automatically.

## Design decisions

- **Why page objects?** When the UI changes, I update one locator in one file instead of every test that touches it.
- **Why `data-test` attributes?** They exist for testing and don't change when designers restyle the page, unlike CSS classes.
- **Why does each test make its own data?** Shared data creates order-dependent tests that pass alone and fail together. Isolated tests can run in parallel.
- **Why schema validation?** A 200 status code with a missing or retyped field is still a broken contract. The schema catches it.
- **Why both Selenium and Playwright?** Many teams run Selenium suites today and are moving to Playwright. Covering the same flows in both shows the trade-offs directly: Playwright's auto-waiting and network control remove a whole class of flaky waits, while Selenium's WebDriver standard still covers the widest range of browsers and grids.
- **Why security tests in a QA suite?** Authorization bugs and injection flaws are functional defects with the highest cost. Checking them on every run, next to the functional tests, catches regressions the day they're introduced instead of at the next annual pen test.
- **Why only a passive ZAP scan?** The baseline scan inspects normal responses (headers, cookies, information leaks) and sends no attack traffic, so it's safe to run against a public demo site. Active scanning belongs only on systems you own or have written permission to test.
- **Why one rerun in CI?** These are shared public demo services that occasionally hiccup. One retry absorbs network noise. A test that fails twice is a real failure.
