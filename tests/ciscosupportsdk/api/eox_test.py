import pytest
from fixtures import *  # noqa

from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.api.eox import EoxError
from ciscosupportsdk.models.eox import EoxAttrib, OSType, SoftwareRelease


@pytest.mark.usefixtures("vcr_config")
class TestEoxApi:
    @pytest.mark.vcr()
    def test_get_by_dates(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.eox.get_by_dates(
                "2022-01-01", "2022-01-31", [EoxAttrib.EO_LAST_SUPPORT_DATE]
            )
        )
        assert count == 2183

    @pytest.mark.vcr()
    def test_get_by_product_ids(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.eox.get_by_product_ids(
                ["WS-C3850-48XS-E", "WS-C3850-48XS-E-RF"]
            )
        )
        assert count == 2

    @pytest.mark.vcr()
    def test_get_by_serial_number(self, api: CiscoSupportAPI):
        count = sum(1 for _ in api.eox.get_by_serial_number(["FHK0933224R"]))
        assert count == 1

    @pytest.mark.vcr()
    def test_get_by_software_release(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.eox.get_by_software_release(
                [SoftwareRelease(os=OSType.IOS, version="12.2")]
            )
        )
        assert count == 6

    @pytest.mark.vcr()
    def test_eox_error(self, api: CiscoSupportAPI):
        with pytest.raises(EoxError):
            next(api.eox.get_by_serial_number(["not a serial"]))
