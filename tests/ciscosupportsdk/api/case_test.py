import pytest

from ciscosupportsdk.api import CiscoSupportAPI

from fixtures import *  # noqa


@pytest.mark.usefixtures("vcr_config")
class TestCaseApi:
    @pytest.mark.vcr()
    def test_cases_by_user_id(self, api: CiscoSupportAPI):
        count = sum(1 for _ in api.case.get_cases_by_user_id(["mannygar"]))
        assert count == 0

    @pytest.mark.vcr()
    def test_get_case_details(self, api: CiscoSupportAPI):
        case = api.case.get_case_details("692277140")
        assert case.creation_date == "2021-09-30T14:46:09.000Z"

    @pytest.mark.vcr()
    def test_get_cases_by_contract_id(self, api: CiscoSupportAPI):
        count = sum(1 for _ in api.case.get_cases_by_contract_id(["92511831"]))
        assert count == 20

    @pytest.mark.vcr()
    def test_get_case_summary(self, api: CiscoSupportAPI):
        count = sum(1 for _ in api.case.get_case_summary(["692277140"]))
        assert count == 1
