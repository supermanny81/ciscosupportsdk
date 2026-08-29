import pytest

from ciscosupportsdk.api import CiscoSupportAPI
from fakes import FakeOAuth2Client, as_responses, install, load, pages  # noqa


@pytest.fixture
def CS_API_KEY():
    return "DUMMY"


@pytest.fixture
def CS_API_SECRET():
    return "DUMMY"


@pytest.fixture
def api_factory(monkeypatch, CS_API_KEY, CS_API_SECRET):
    """Builds a ``CiscoSupportAPI`` backed by fixture payloads.

    Pass either a fixture name (``"bug/get_bug_details"``), a payload, or a
    list of either -- one entry per expected HTTP call. Returns the API and
    the fake client, so tests can assert on the requests that were made.
    """

    def _make(source, status_code: int = 200):
        if isinstance(source, str):
            payloads = pages(source)
        elif isinstance(source, dict):
            payloads = [source]
        else:
            payloads = []
            for item in source:
                payloads.extend(
                    pages(item) if isinstance(item, str) else [item]
                )

        client = install(monkeypatch, as_responses(payloads, status_code))
        return CiscoSupportAPI(CS_API_KEY, CS_API_SECRET), client

    return _make


@pytest.fixture
def api(api_factory):
    """A ``CiscoSupportAPI`` with no queued responses.

    Useful for tests that install their own payloads via ``api_factory``.
    """
    return api_factory([])[0]
