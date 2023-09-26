import pytest
from fixtures import *  # noqa

from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.models.bug import Bug, DateModified, SortBy


@pytest.mark.usefixtures("vcr_config")
class TestBugApi:
    @pytest.mark.vcr()
    def test_get_bug_details(self, api: CiscoSupportAPI):
        details: Bug = next(api.bug.get_bug_details(["CSCvc57217"]))
        assert details.bug_id == "CSCvc57217"
        assert details.base_pid is None

    @pytest.mark.vcr()
    def test_get_bugs_by_product_id(self, api: CiscoSupportAPI):
        count = 0
        for item in api.bug.get_bugs_by_product_id(
            "WS-C3560-48PS-S", sort_by=SortBy.SEVERITY
        ):
            count += 1

        assert count == 3

    @pytest.mark.vcr()
    def test_get_bugs_by_product_id_and_release(self, api: CiscoSupportAPI):
        count = 0
        for bug in api.bug.get_bugs_by_product_id_and_release(
            "WS-C3560-48PS-S", ["15.2(03)E01"]
        ):
            count += 1
        assert count == 0

    @pytest.mark.vcr()
    def test_get_bugs_by_keyword(self, api: CiscoSupportAPI):
        count = 0
        for bug in api.bug.get_bugs_by_keyword("IOS SSH PKI"):
            count += 1
        assert count == 3

    @pytest.mark.vcr()
    def test_get_bugs_by_product_and_affected_release(
        self, api: CiscoSupportAPI
    ):
        count = 0
        for bug in api.bug.get_bugs_by_product_and_affected_release(
            "Cisco 5500 Series Wireless Controllers",
            ["7.4(100.0)"],
            modified_date=DateModified.ALL,
        ):
            count += 1
        assert count == 0

    @pytest.mark.vcr()
    def test_get_bugs_by_product_and_fixed_release(self, api: CiscoSupportAPI):
        count = 0
        for bug in api.bug.get_bugs_by_product_and_fixed_release(
            "Cisco 5500 Series Wireless Controllers",
            ["7.6(100.6)"],
            modified_date=DateModified.ALL,
        ):
            count += 1
        assert count == 0

    @pytest.mark.vcr()
    def test_get_bugs_by_product_name_and_affected_release(
        self, api: CiscoSupportAPI
    ):
        count = 0
        for bug in api.bug.get_bugs_by_product_name_and_affected_release(
            "Cisco Unity Connection Version 10.5",
            ["10.5(2)"],
            modified_date=DateModified.ALL,
        ):
            count += 1
        assert count == 248

    @pytest.mark.vcr()
    def test_get_bugs_by_product_name_and_fixed_release(
        self, api: CiscoSupportAPI
    ):
        count = 0
        for bug in api.bug.get_bugs_by_product_name_and_fixed_release(
            "Cisco Unified Communications Manager (CallManager)",
            ["10.5(2)"],
            modified_date=DateModified.ALL,
        ):
            count += 1
        assert count == 0
