import os

import pytest

from ciscosupportsdk.api import CiscoSupportAPI


@pytest.fixture
def CS_API_KEY():
    return os.getenv("CS_API_KEY", "DUMMY")


@pytest.fixture
def CS_API_SECRET():
    return os.getenv("CS_API_SECRET", "DUMMY")


@pytest.fixture
def api(CS_API_KEY: str, CS_API_SECRET: str) -> CiscoSupportAPI:
    return CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("Authorization", "DUMMY")],
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    return os.path.join("tests/cassettes", request.module.__name__)
