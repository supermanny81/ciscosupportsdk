import pytest
from fixtures import *  # noqa

from ciscosupportsdk.api import CiscoSupportAPI
from ciscosupportsdk.models.case import CaseDetailResponse


class TestCaseModel:
    def test_sparse_open_case_details(self):
        """
        Regression for cases whose payloads omit state-dependent fields.

        Open cases (e.g. 701071708) arrive without ``close_date`` and other
        fields the API only populates for certain states. The model must
        validate such sparse payloads instead of raising ValidationError, so
        downstream consumers no longer need to bypass the SDK's parsing.
        """
        payload = {
            "caseDetail": {
                "case_id": "701071708",
                "title": "Open case with a sparse payload",
                "creation_date": "2024-01-02T03:04:05.000Z",
            }
        }

        case = CaseDetailResponse(**payload).items

        assert case.case_id == "701071708"
        # Omitted scalars fall back to None ...
        assert case.close_date is None
        assert case.item_entry_id is None
        assert case.status_flag is None
        assert case.crashinfo is None
        # ... and omitted collections default to empty lists so they stay
        # iterable for consumers.
        assert case.bugs == []
        assert case.rmas == []
        assert case.notes == []
        assert case.rma_numbers == []


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
        assert count == 10

    @pytest.mark.vcr()
    def test_get_case_summary(self, api: CiscoSupportAPI):
        count = sum(1 for _ in api.case.get_case_summary(["692277140"]))
        assert count == 1
