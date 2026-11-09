"""API security checks: authentication and authorization must hold for every write
operation, and hostile input must never be rewarded with a token."""

import pytest

from api_client import BookingClient
from test_data.factories import booking_payload

pytestmark = pytest.mark.security


@pytest.mark.smoke
def test_delete_without_token_is_rejected(api, booking):
    booking_id, _ = booking
    assert api.delete_booking(booking_id).status_code == 403
    assert api.get_booking(booking_id).status_code == 200, "Booking must survive the attempt"


@pytest.mark.regression
def test_partial_update_without_token_is_rejected(api, booking):
    booking_id, original = booking
    assert api.partial_update_booking(booking_id, {"firstname": "Intruder"}).status_code == 403
    assert api.get_booking(booking_id).json() == original, "Data must be unchanged"


@pytest.mark.regression
def test_forged_token_is_rejected(booking):
    booking_id, _ = booking
    attacker = BookingClient()
    attacker.session.headers.update({"Cookie": "token=forged0123456789"})
    response = attacker.update_booking(booking_id, booking_payload(firstname="Forged"))
    assert response.status_code == 403


@pytest.mark.regression
def test_wrong_basic_auth_is_rejected(booking):
    booking_id, _ = booking
    attacker = BookingClient()
    attacker.session.auth = ("admin", "not-the-password")
    assert attacker.delete_booking(booking_id).status_code == 403


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password",
    [
        ("admin' OR '1'='1", "anything"),
        ("admin'--", "anything"),
        ("admin", "' OR '1'='1"),
    ],
    ids=["sqli-or-true", "sqli-comment", "sqli-in-password"],
)
def test_injection_style_credentials_get_no_token(api, username, password):
    body = api.create_token(username, password).json()
    assert "token" not in body
