import pytest


from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.models.serialnumbertoinformation import CoverageStatus

from fixtures import *  # noqa


@pytest.mark.usefixtures("vcr_config")
class TestSerialNumberToInfoApi:
    @pytest.mark.vcr
    def test_get_coverage_status(self, api: CiscoSupportAPI):
        status: CoverageStatus = next(
            api.serial_information.get_coverage_status(["FXS2130Q286"])
        )
        assert status.is_covered is True
        assert status.coverage_end_date == "2023-12-31"
        assert status.serial_number == "FXS2130Q286"

    @pytest.mark.vcr
    def test_get_coverage_summary_by_serial(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.serial_information.get_coverage_summary_by_serial(
                ["FXS2130Q286"]
            )
        )
        assert count == 1

    @pytest.mark.skip(
        reason="need to find another instance number to test with."
    )
    @pytest.mark.vcr
    def test_get_coverage_summary_by_instance(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.serial_information.get_coverage_summary_by_instance(
                ["203920501"]
            )
        )
        assert count == 1

    @pytest.mark.vcr
    def test_get_orderable_pids(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.serial_information.get_orderable_pids(
                ["FOC0717W107", "FOC11517LEX", "FOC0737Y43K"]
            )
        )
        assert count == 3

    @pytest.mark.vcr
    def test_get_coverage_owner_status(self, api: CiscoSupportAPI):
        count = sum(
            1
            for _ in api.serial_information.get_coverage_owner_status(
                ["FXS2130Q286"]
            )
        )
        assert count == 1
