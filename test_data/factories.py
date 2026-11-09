"""Test data builders. Each test creates the data it needs, so tests never depend on
each other or on whatever happens to be in the shared environment."""

import uuid
from datetime import UTC, datetime, timedelta


def booking_payload(**overrides) -> dict:
    checkin = datetime.now(UTC).date() + timedelta(days=30)
    payload = {
        "firstname": "QA",
        "lastname": f"Auto-{uuid.uuid4().hex[:8]}",
        "totalprice": 245,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": (checkin + timedelta(days=3)).isoformat(),
        },
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload


CHECKOUT_CUSTOMER = {"first": "Test", "last": "Customer", "postal_code": "67202"}
