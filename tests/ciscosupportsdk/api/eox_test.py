import pytest

from ciscosupportsdk.api.eox import EoxError
from ciscosupportsdk.models.eox import EoxAttrib, OSType, SoftwareRelease
from fixtures import *  # noqa


class TestEoxApi:
    def test_get_by_dates(self, api_factory):
        # Three pages; EoX paginates via its own PascalCase envelope.
        api, client = api_factory("eox/get_by_dates")

        count = sum(
            1
            for _ in api.eox.get_by_dates(
                "2022-01-01", "2022-01-31", [EoxAttrib.EO_LAST_SUPPORT_DATE]
            )
        )

        assert count == 9
        assert len(client.requests) == 3
        assert client.params()["eoxAttrib"] == "EO_LAST_SUPPORT_DATE"
        assert client.params()["responseencoding"] == "json"

    def test_get_by_product_ids(self, api_factory):
        api, client = api_factory("eox/get_by_product_ids")

        count = sum(
            1
            for _ in api.eox.get_by_product_ids(
                ["WS-C3850-48XS-E", "WS-C3850-48XS-E-RF"]
            )
        )

        assert count == 2
        assert "WS-C3850-48XS-E,WS-C3850-48XS-E-RF" in client.urls[0]

    def test_get_by_serial_number(self, api_factory):
        api, _ = api_factory("eox/get_by_serial_number")

        count = sum(1 for _ in api.eox.get_by_serial_number(["FHK6666FFFF"]))

        assert count == 1

    def test_get_by_software_release(self, api_factory):
        api, client = api_factory("eox/get_by_software_release")

        count = sum(
            1
            for _ in api.eox.get_by_software_release(
                [SoftwareRelease(os=OSType.IOS, version="12.2")]
            )
        )

        assert count == 9
        # Release strings go over as "<version>,<os>" in input1..input20.
        assert client.params()["input1"] == "12.2,IOS"

    def test_eox_error(self, api_factory):
        api, _ = api_factory("eox/eox_error")

        with pytest.raises(EoxError):
            next(api.eox.get_by_serial_number(["not a serial"]))

    def test_record_without_migration_details(self, api_factory):
        api, _ = api_factory("eox/get_by_serial_number")

        record = next(api.eox.get_by_serial_number(["FHK6666FFFF"]))

        assert record.eol_product_id
        # Dates come back as an object with an empty string when unset.
        assert record.end_of_sale_date.to_date().year == 2007
