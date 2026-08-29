"""
A fake HTTP transport for the Support API tests.

The SDK is exercised against JSON fixtures rather than recorded HTTP traffic.
The fake is installed in place of authlib's ``OAuth2Session``, so everything
above the socket -- token handling, retry and status-code logic, query
parameter construction, pagination and model parsing -- runs for real. Only
the wire is replaced.

Fixtures live in ``tests/fixtures/<api>/<name>.json`` and were derived from
real API responses, with identifying values replaced and long record sets
trimmed. Public Cisco data (bug identifiers, product identifiers, EoX
lifecycle records) is unmodified.
"""

import copy
import json
import pathlib

FIXTURE_ROOT = pathlib.Path(__file__).parent.parent / "fixtures"


def load(name: str):
    """Loads ``tests/fixtures/<name>.json``.

    A fixture holding a list of pages is returned as a list; a single-page
    fixture is returned as one dict.
    """
    path = FIXTURE_ROOT / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"No fixture at {path}")
    return json.loads(path.read_text())


def pages(name: str) -> list:
    """Loads a fixture and always returns a list of pages."""
    data = load(name)
    return data if isinstance(data, list) else [data]


class FakeToken(dict):
    """Stands in for authlib's OAuth2Token."""

    def __init__(self, expired: bool = False, **kwargs):
        super().__init__(access_token="DUMMY", token_type="Bearer", **kwargs)
        self._expired = expired

    def is_expired(self):
        return self._expired


class FakeResponse:
    def __init__(self, payload=None, status_code: int = 200, headers=None):
        self.status_code = status_code
        self._payload = {} if payload is None else payload
        self.headers = headers or {}

    @property
    def content(self) -> bytes:
        return json.dumps(self._payload).encode()

    def json(self):
        return self._payload


class FakeOAuth2Client:
    """Replaces ``OAuth2Session``; serves queued responses in order.

    Every request is recorded in ``requests`` as ``(method, url, kwargs)`` so
    tests can assert on the URL and query string the SDK built.
    """

    def __init__(self, responses):
        self._responses = list(responses)
        self.requests = []
        self.token_fetches = 0
        self.token = FakeToken()

    def fetch_token(self, url, **kwargs):
        self.token_fetches += 1
        self.token = FakeToken()
        return self.token

    def request(self, method, url, **kwargs):
        # Snapshot the kwargs: callers reuse and mutate their params dict
        # between pages, which would otherwise rewrite history on requests
        # already recorded.
        self.requests.append((method, url, copy.deepcopy(kwargs)))
        if not self._responses:
            raise AssertionError(
                f"Unexpected request: {method} {url} "
                f"(fixture responses exhausted)"
            )
        return self._responses.pop(0)

    # -- assertion helpers ------------------------------------------------

    @property
    def urls(self) -> list:
        return [url for _, url, _ in self.requests]

    def params(self, index: int = 0) -> dict:
        return self.requests[index][2].get("params") or {}

    def body(self, index: int = 0) -> dict:
        return self.requests[index][2].get("json") or {}


def as_responses(payloads, status_code: int = 200) -> list:
    """Wraps fixture payloads as ``FakeResponse`` objects."""
    if isinstance(payloads, dict):
        payloads = [payloads]
    return [FakeResponse(p, status_code) for p in payloads]


def install(monkeypatch, responses) -> FakeOAuth2Client:
    """Swaps ``OAuth2Session`` for a fake serving ``responses``."""
    client = FakeOAuth2Client(responses)
    monkeypatch.setattr(
        "ciscosupportsdk.apisession.OAuth2Session",
        lambda *a, **kw: client,
    )
    return client
