import pytest

from ciscosupportsdk.apisession import ApiError, ApiSession
from fixtures import *  # noqa


class TestApiSession:
    def test_auth_success(self, api_factory):
        _, client = api_factory([])

        # The session fetches exactly one token when it is constructed.
        assert client.token_fetches == 1

    def test_api_error(self, api_factory):
        api, _ = api_factory("apisession/api_error", status_code=400)

        with pytest.raises(ApiError):
            api._session._get(
                "/bug/v2.0/bugs/product_name/"
                "Cisco Unified Communications Manager "
                "(CallManager)/fixed_in_releases",
                params={},
            )

    def test_error_payload_is_surfaced(self, api_factory):
        api, _ = api_factory("apisession/api_error", status_code=400)

        with pytest.raises(ApiError, match="400"):
            api._session._get("/bug/v2.0/bugs/bug_ids/CSCxx00000", params={})

    def test_base_url_is_applied(self, monkeypatch):
        client = install(monkeypatch, as_responses([{}]))  # noqa: F405
        session = ApiSession("id", "secret", base_url="https://example.test")

        session._get("/thing", {})

        assert client.urls[0] == "https://example.test/thing"
