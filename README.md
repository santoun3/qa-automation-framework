# QA Automation Framework — UI + API

[![Tests](https://github.com/YOUR-GITHUB-USERNAME/qa-automation-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR-GITHUB-USERNAME/qa-automation-framework/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Selenium](https://img.shields.io/badge/selenium-4-43B02A)
![pytest](https://img.shields.io/badge/pytest-8-0A9EDC)

A test automation framework built the way I build them for production teams: page objects,
independent tests, data-driven cases, contract checks on the API, and a CI pipeline that runs
fast smoke tests on every push and the full regression suite nightly.

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
| Data-driven testing with `pytest.mark.parametrize` | `tests/ui/test_login.py`, `tests/ui/test_checkout.py` |
| End-to-end critical path, including a price-integrity check | `tests/ui/test_checkout.py` |
| API contract testing with JSON Schema | `api_client/schemas.py`, `tests/api/test_bookings.py` |
| Negative and security checks (bad credentials, missing auth token) | `tests/api/test_auth.py` |
| Test isolation: every test creates and cleans up its own data | `conftest.py` (`booking` fixture), `test_data/factories.py` |
| Screenshot and URL embedded in the report on any UI failure | `conftest.py` |
| Environment-driven config: same suite, any environment | `config/settings.py` |
| CI/CD: parallel runs, smoke vs. regression scope, HTML + JUnit reports | `.github/workflows/tests.yml` |

## Test coverage

| Area | Tests | Covers |
| --- | --- | --- |
| UI · Login | 5 | Valid login, locked-out user, wrong password, missing fields |
| UI · Catalog | 6 | Product count, 4 sort orders, cart badge add/remove |
| UI · Checkout | 4 | Full purchase with total verification, 3 required-field validations |
| API · Auth | 4 | Health check, token issue, bad credentials, update without token (403) |
| API · Bookings | 7 | Create, read, filter, full update, partial update, delete, unknown ID (404) |
| **Total** | **26** | |

## Project structure

```
├── .github/workflows/tests.yml   # CI: smoke on push/PR, full regression nightly
├── api_client/
│   ├── booking_client.py         # API wrapper: URLs, headers and auth in one place
│   └── schemas.py                # JSON Schemas for contract tests
├── config/settings.py            # All settings overridable by environment variable
├── pages/                        # Page objects (base, login, inventory, cart, checkout)
├── test_data/factories.py        # Unique test data per run
├── tests/
│   ├── api/                      # REST API tests
│   └── ui/                       # Browser tests
├── conftest.py                   # Fixtures, setup/teardown, failure screenshots
└── pytest.ini                    # Markers: ui, api, smoke, regression
```

## Run it locally

Requires Python 3.10+ and Chrome.

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/qa-automation-framework.git
cd qa-automation-framework
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                         # everything
pytest -m smoke                # fast critical-path checks
pytest -m api                  # API only
pytest -m "ui and regression"  # combine markers
pytest -n auto                 # run in parallel
HEADLESS=false pytest -m ui    # watch the browser
pytest --html=reports/report.html --self-contained-html   # HTML report
```

Selenium Manager downloads the matching ChromeDriver automatically.

## Design decisions

- **Why page objects?** When the UI changes, I update one locator in one file instead of every test that touches it.
- **Why `data-test` attributes?** They exist for testing and don't change when designers restyle the page, unlike CSS classes.
- **Why does each test make its own data?** Shared data creates order-dependent tests that pass alone and fail together. Isolated tests can run in parallel.
- **Why schema validation?** A 200 status code with a missing or retyped field is still a broken contract. The schema catches it.
- **Why one rerun in CI?** These are shared public demo services that occasionally hiccup. One retry absorbs network noise. A test that fails twice is a real failure.
