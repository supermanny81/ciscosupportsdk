"""
Session level behaviour: token refresh, throttling, and query parameter
isolation between calls. These drive ``ApiSession`` directly rather than
through one of the API wrappers.
"""

from typing import List, Optional

import pytest
from pydantic import BaseModel, Field

from ciscosupportsdk.apisession import (
    DEFAULT_RETRY_AFTER,
    ApiError,
    ApiSession,
    RateLimitError,
)
from ciscosupportsdk.models.common import ApiResponse, CamelCaseApi
from fakes import FakeResponse, FakeToken, install


@pytest.fixture
def session_factory(monkeypatch):
    def _make(responses, **kwargs):
        client = install(monkeypatch, responses)
        return ApiSession("id", "secret", **kwargs), client

    return _make


class TestTokenHandling:
    def test_valid_token_is_not_refetched(self, session_factory):
        # ``is_expired`` is a method on authlib >= 1.3. Reading it without
        # calling it is always truthy, which re-fetched a token before every
        # single request.
        session, client = session_factory(
            [FakeResponse({"ok": True}, 200)] * 3
        )
        fetches_after_init = client.token_fetches

        for _ in range(3):
            session._get("/thing", {})

        assert client.token_fetches == fetches_after_init

    def test_expired_token_is_refetched(self, session_factory):
        session, client = session_factory([FakeResponse({"ok": True}, 200)])
        client.token = FakeToken(expired=True)
        fetches_after_init = client.token_fetches

        session._get("/thing", {})

        assert client.token_fetches == fetches_after_init + 1

    def test_rejected_token_is_refreshed_once(self, session_factory):
        session, client = session_factory(
            [FakeResponse(status_code=401), FakeResponse({"ok": True}, 200)]
        )

        assert session._get("/thing", {}) == {"ok": True}
        assert len(client.requests) == 2

    def test_persistent_401_raises(self, session_factory):
        session, _ = session_factory(
            [FakeResponse(status_code=401), FakeResponse(status_code=401)]
        )

        with pytest.raises(ApiError):
            session._get("/thing", {})

    def test_no_retries_configured_still_raises(self, session_factory):
        # With max_retries=0 the loop must not fall through returning None.
        session, _ = session_factory(
            [FakeResponse(status_code=401), FakeResponse(status_code=401)],
            max_retries=0,
        )

        with pytest.raises(ApiError):
            session._get("/thing", {})


class TestThrottling:
    def test_429_is_retried(self, session_factory, monkeypatch):
        monkeypatch.setattr(
            "ciscosupportsdk.apisession.time.sleep", lambda s: None
        )
        session, client = session_factory(
            [
                FakeResponse(status_code=429, headers={"Retry-After": "0"}),
                FakeResponse({"ok": True}, 200),
            ]
        )

        assert session._get("/thing", {}) == {"ok": True}
        assert len(client.requests) == 2

    def test_persistent_429_raises_rate_limit_error(
        self, session_factory, monkeypatch
    ):
        monkeypatch.setattr(
            "ciscosupportsdk.apisession.time.sleep", lambda s: None
        )
        session, _ = session_factory(
            [FakeResponse(status_code=429, headers={"Retry-After": "7"})] * 3,
            max_retries=2,
        )

        with pytest.raises(RateLimitError) as exc:
            session._get("/thing", {})

        assert exc.value.retry_after == 7.0


class Thing(BaseModel):
    name: Optional[str] = None


class SnakeResponse(ApiResponse):
    items: List[Thing] = Field(default_factory=list, alias="things")


class CamelResponse(ApiResponse, CamelCaseApi):
    items: List[Thing] = Field(default_factory=list, alias="things")


class TestQueryParamIsolation:
    def test_page_param_does_not_leak_between_calls(self, session_factory):
        # ``query_params`` used to default to a shared mutable dict, so a
        # camelCase endpoint left ``pageIndex`` behind for the next
        # snake_case call to send as well.
        session, client = session_factory(
            [FakeResponse({"things": []}, 200)] * 2
        )

        list(session.enumerate_results(CamelResponse, "/camel"))
        list(session.enumerate_results(SnakeResponse, "/snake"))

        assert client.requests[0][2]["params"] == {"pageIndex": 1}
        assert client.requests[1][2]["params"] == {"page_index": 1}

    def test_callers_dict_is_not_mutated(self, session_factory):
        session, _ = session_factory([FakeResponse({"things": []}, 200)])
        params = {"status": "O"}

        list(session.enumerate_results(SnakeResponse, "/snake", params))

        assert params == {"status": "O"}

    def test_base_url_override_is_honoured(self, session_factory):
        session, client = session_factory(
            [FakeResponse({}, 200)], base_url="https://example.invalid"
        )

        session._get("/thing", {})

        assert client.requests[0][1] == "https://example.invalid/thing"


class TestRetryAfter:
    def test_missing_header_uses_default_backoff(self, session_factory):
        session, _ = session_factory([FakeResponse({"ok": True}, 200)])

        assert session._retry_after(FakeResponse()) == DEFAULT_RETRY_AFTER

    def test_http_date_header_falls_back(self, session_factory):
        # Retry-After may be an HTTP date rather than a number of seconds.
        # We do not parse those; the default backoff is used instead.
        session, _ = session_factory([FakeResponse({"ok": True}, 200)])
        response = FakeResponse(
            headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}
        )

        assert session._retry_after(response) == DEFAULT_RETRY_AFTER

    def test_negative_header_is_clamped(self, session_factory):
        session, _ = session_factory([FakeResponse({"ok": True}, 200)])

        assert (
            session._retry_after(FakeResponse(headers={"Retry-After": "-5"}))
            == 0.0
        )


class TestMissingToken:
    def test_empty_token_is_fetched_before_the_request(self, session_factory):
        session, client = session_factory([FakeResponse({"ok": True}, 200)])
        # An empty token is falsy; is_expired() must not even be consulted.
        client.token = {}
        fetches_after_init = client.token_fetches

        session._get("/thing", {})

        assert client.token_fetches == fetches_after_init + 1


class TestPost:
    def test_post_sends_a_json_body(self, session_factory):
        session, client = session_factory([FakeResponse({"ok": True}, 200)])

        result = session._post("/thing", json={"pid": "ASR1000"})

        assert result == {"ok": True}
        method, url, kwargs = client.requests[0]
        assert method == "POST"
        assert url.endswith("/thing")
        assert kwargs["json"] == {"pid": "ASR1000"}

    def test_post_surfaces_errors(self, session_factory):
        session, _ = session_factory([FakeResponse({}, 400)])

        with pytest.raises(ApiError):
            session._post("/thing", json={})
