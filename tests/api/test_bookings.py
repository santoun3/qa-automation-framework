import pytest
from jsonschema import validate

from api_client import schemas
from test_data.factories import booking_payload

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_create_booking_returns_the_saved_record(authed_api):
    payload = booking_payload()
    response = authed_api.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    validate(body, schemas.CREATE_BOOKING_RESPONSE)
    assert body["booking"] == payload

    authed_api.delete_booking(body["bookingid"])


@pytest.mark.regression
def test_get_booking_matches_what_was_created(api, booking):
    booking_id, payload = booking
    response = api.get_booking(booking_id)

    assert response.status_code == 200
    validate(response.json(), schemas.BOOKING)
    assert response.json() == payload


@pytest.mark.regression
def test_bookings_can_be_filtered_by_name(api, booking):
    booking_id, payload = booking
    response = api.list_bookings(firstname=payload["firstname"], lastname=payload["lastname"])

    assert response.status_code == 200
    validate(response.json(), schemas.BOOKING_ID_LIST)
    assert booking_id in [b["bookingid"] for b in response.json()]


@pytest.mark.regression
def test_full_update_replaces_every_field(authed_api, booking):
    booking_id, _ = booking
    updated = booking_payload(firstname="Updated", totalprice=500, depositpaid=False)

    response = authed_api.update_booking(booking_id, updated)
    assert response.status_code == 200
    assert response.json() == updated


@pytest.mark.regression
def test_partial_update_changes_only_the_given_fields(authed_api, booking):
    booking_id, original = booking

    response = authed_api.partial_update_booking(booking_id, {"additionalneeds": "Late checkout"})
    assert response.status_code == 200
    assert response.json() == {**original, "additionalneeds": "Late checkout"}


@pytest.mark.regression
def test_deleted_booking_is_gone(authed_api):
    booking_id = authed_api.create_booking(booking_payload()).json()["bookingid"]

    assert authed_api.delete_booking(booking_id).status_code == 201
    assert authed_api.get_booking(booking_id).status_code == 404


@pytest.mark.regression
def test_unknown_booking_returns_404(api):
    assert api.get_booking(999_999_999).status_code == 404
