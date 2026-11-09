"""Thin client for the Restful Booker API.

Tests call methods like create_booking() instead of building raw requests, which keeps
URLs, headers, and auth in one place and keeps tests readable."""

import requests

from config import settings


class BookingClient:
    def __init__(self, base_url: str = settings.API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", settings.API_TIMEOUT_SECONDS)
        return self.session.request(method, self._url(path), **kwargs)

    # --- Auth -----------------------------------------------------------
    def create_token(self, username: str, password: str) -> requests.Response:
        return self._request("POST", "/auth", json={"username": username, "password": password})

    def authenticate(self) -> str:
        response = self.create_token(settings.API_ADMIN_USER, settings.API_ADMIN_PASSWORD)
        token = response.json()["token"]
        self.session.headers.update({"Cookie": f"token={token}"})
        return token

    # --- Health ---------------------------------------------------------
    def ping(self) -> requests.Response:
        return self._request("GET", "/ping")

    # --- Bookings -------------------------------------------------------
    def list_bookings(self, **filters) -> requests.Response:
        return self._request("GET", "/booking", params=filters)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self._request("GET", f"/booking/{booking_id}")

    def create_booking(self, payload: dict) -> requests.Response:
        return self._request("POST", "/booking", json=payload)

    def update_booking(self, booking_id: int, payload: dict) -> requests.Response:
        return self._request("PUT", f"/booking/{booking_id}", json=payload)

    def partial_update_booking(self, booking_id: int, payload: dict) -> requests.Response:
        return self._request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id: int) -> requests.Response:
        return self._request("DELETE", f"/booking/{booking_id}")
