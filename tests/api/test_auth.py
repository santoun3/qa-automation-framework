import pytest

from config import settings

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_service_health_check(api):
    assert api.ping().status_code == 201


@pytest.mark.smoke
def test_valid_credentials_return_a_token(api):
    response = api.create_token(settings.API_ADMIN_USER, settings.API_ADMIN_PASSWORD)
    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str) and token


@pytest.mark.regression
def test_invalid_credentials_return_no_token(api):
    response = api.create_token("admin", "not-the-password")
    body = response.json()
    assert "token" not in body
    assert body.get("reason") == "Bad credentials"


@pytest.mark.regression
def test_update_without_token_is_rejected(api, booking):
    booking_id, payload = booking
    response = api.update_booking(booking_id, {**payload, "firstname": "Intruder"})
    assert response.status_code == 403
