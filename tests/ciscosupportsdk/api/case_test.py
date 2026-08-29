import pytest

from ciscosupportsdk.models.case import (
    CaseDetail,
    CaseDetailResponse,
    CaseStatusFlag,
    SortCaseBy,
)
from fixtures import *  # noqa


class TestCaseModel:
    def test_sparse_open_case_details(self):
        """
        An open case omits the fields that only apply once it is closed, and
        the summary-only fields the detail endpoint does not return at all.
        The model must validate such sparse payloads instead of raising
        ValidationError, so downstream consumers no longer need to bypass the
        SDK's parsing.
        """
        payload = {
            "caseDetail": {
                "case_id": "600000001",
                "title": "Open case with a sparse payload",
                "creation_date": "2024-01-02T03:04:05.000Z",
            }
        }

        case = CaseDetailResponse(**payload).items

        assert case.case_id == "600000001"
        # Omitted scalars fall back to None ...
        assert case.close_date is None
        assert case.item_entry_id is None
        assert case.status_flag is None
        # ... and omitted collections default to empty lists so they stay
        # iterable for consumers.
        assert case.bugs == []
        assert case.rmas == []
        assert case.notes == []


class TestCaseApi:
    def test_cases_by_user_id(self, api_factory):
        api, client = api_factory("case/cases_by_user_id")

        count = sum(1 for _ in api.case.get_cases_by_user_id(["testuser"]))

        assert count == 0
        assert client.params()["sort_by"] == SortCaseBy.UPDATED_DATE
        assert client.params()["status_flag"] == CaseStatusFlag.OPEN

    def test_get_case_details(self, api_factory):
        api, client = api_factory("case/get_case_details")

        case: CaseDetail = api.case.get_case_details("600000001")

        assert case.creation_date == "2021-09-30T14:46:09.000Z"
        assert case.close_date is not None
        assert case.notes
        # The live detail payload omits these two entirely; they must not
        # be required fields.
        assert case.item_entry_id is None
        assert case.status_flag is None
        assert "/cases/details/case_id/600000001" in client.urls[0]

    def test_get_cases_by_contract_id(self, api_factory):
        api, client = api_factory("case/get_cases_by_contract_id")

        cases = list(api.case.get_cases_by_contract_id(["10000001"]))

        assert len(cases) == 1
        assert cases[0].contract_id == "10000001"
        assert cases[0].rmas == ["800000003", "800000004"]
        assert client.params()["sort_by"] == SortCaseBy.UPDATED_DATE

    def test_get_cases_by_contract_id_honours_sort_by(self, api_factory):
        api, client = api_factory("case/get_cases_by_contract_id")

        list(
            api.case.get_cases_by_contract_id(
                ["10000001"], sort_by=SortCaseBy.STATUS
            )
        )

        assert client.params()["sort_by"] == SortCaseBy.STATUS

    def test_get_case_summary(self, api_factory):
        api, _ = api_factory("case/get_case_summary")

        cases = list(api.case.get_case_summary(["600000001"]))

        assert len(cases) == 1
        assert cases[0].case_id == "600000001"

    def test_date_range_is_validated(self, api):
        # The documented maximum range for case searches is 90 days.
        with pytest.raises(ValueError, match="exceeds the maximum"):
            list(
                api.case.get_cases_by_user_id(
                    ["testuser"],
                    date_created_from="2024-01-01T00:00:00Z",
                    date_created_to="2024-12-01T00:00:00Z",
                )
            )
