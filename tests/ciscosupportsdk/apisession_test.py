import pytest
from authlib.integrations.base_client.errors import OAuthError
from fixtures import *  # noqa

from ciscosupportsdk.api import ApiSession
from ciscosupportsdk.apisession import ApiError


@pytest.mark.usefixtures("vcr_config")
class TestApiSession:
    @pytest.mark.skip(
        "Expected an OAuth failure, need to investigate "
        "why this behavior changed."
    )
    def test_auth_failure(self):
        print(ApiSession("USE", "ME"))
        with pytest.raises(OAuthError):
            print(ApiSession("NOT_A_KEY", "NOT_A_SECRET"))

    @pytest.mark.vcr()
    def test_auth_success(self, CS_API_KEY, CS_API_SECRET):
        ApiSession(CS_API_KEY, CS_API_SECRET)

    @pytest.mark.vcr()
    def test_api_error(self, CS_API_KEY, CS_API_SECRET):
        api = ApiSession(CS_API_KEY, CS_API_SECRET)
        with pytest.raises(ApiError):
            api._get(
                "/bug/v2.0/bugs/product_name/"
                "Cisco Unified Communications Manager "
                "(CallManager)/fixed_in_releases",
                params={},
            )
