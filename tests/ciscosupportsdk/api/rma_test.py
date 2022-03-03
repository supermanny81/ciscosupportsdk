import pytest


from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.apisession import ApiError
from ciscosupportsdk.models.serviceorderreturn import Rma, User

from fixtures import *  # noqa


@pytest.mark.usefixtures("vcr_config")
class TestRmaApi:
    @pytest.mark.vcr
    def test_raise_api_error(self, api: CiscoSupportAPI):
        with pytest.raises(ApiError):
            next(api.rma.get_rma_details_by_rma_number("84894022"))

    @pytest.mark.vcr
    def test_rma_details(self, api: CiscoSupportAPI):
        rma: Rma = next(api.rma.get_rma_details_by_rma_number("801934965"))
        assert rma.case_id == "692541209"

    @pytest.mark.vcr
    def test_rma_by_user_id_fail(self, api: CiscoSupportAPI):
        with pytest.raises(ApiError):
            next(api.rma.get_rma_details_by_user_id("mannygar"))

    @pytest.mark.skip("need to find a user with lots of RMAs")
    def test_rma_by_user_id(self, api: CiscoSupportAPI):
        next(
            api.rma.get_rma_details_by_user_id(
                "????", "2021-12-01", "2021-12-15"
            )
        )
