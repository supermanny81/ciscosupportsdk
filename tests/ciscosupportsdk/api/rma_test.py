import pytest

from ciscosupportsdk.apisession import ApiError
from ciscosupportsdk.models.serviceorderreturn import Rma
from fixtures import *  # noqa


class TestRmaApi:
    def test_rma_details(self, api_factory):
        api, client = api_factory("rma/rma_details")

        rma: Rma = next(api.rma.get_rma_details_by_rma_number("800000001"))

        assert rma.rma_no == 800000001
        assert rma.case_id == "600000003"
        assert rma.status == "Closed"
        # RMA is a camelCase API, so it must be paged with pageIndex.
        assert client.params() == {"pageIndex": 1}

    def test_raise_api_error(self, api_factory):
        api, _ = api_factory("rma/raise_api_error")

        with pytest.raises(ApiError):
            next(api.rma.get_rma_details_by_rma_number("800000002"))

    def test_rma_by_user_id_fail(self, api_factory):
        api, _ = api_factory("rma/rma_by_user_id_fail")

        with pytest.raises(ApiError):
            next(api.rma.get_rma_details_by_user_id("testuser"))

    def test_date_range_is_validated(self, api):
        # The documented maximum range for an RMA search is 30 days.
        with pytest.raises(ValueError, match="exceeds the maximum"):
            next(
                api.rma.get_rma_details_by_user_id(
                    "testuser", "2021-12-01", "2022-03-01"
                )
            )

    def test_inverted_date_range_is_rejected(self, api):
        with pytest.raises(ValueError, match="precedes start date"):
            next(
                api.rma.get_rma_details_by_user_id(
                    "testuser", "2021-12-15", "2021-12-01"
                )
            )

    def test_rma_details_by_user_id_pages(self, api_factory):
        # Previously unskippable: it needed a user with many RMAs. The paging
        # loop used to compare against page_records and never advanced its
        # cursor, so it could not terminate.
        def page(index, last, rma_no):
            return {
                "OrderList": {
                    "APIPagination": {
                        "pageIndex": index,
                        "lastIndex": last,
                        "totalRecords": 2,
                        "pageRecords": 1,
                    },
                    "users": [
                        {
                            "userId": "testuser",
                            "returnCount": "2",
                            "returns": [{"rmaNo": rma_no, "status": "Open"}],
                        }
                    ],
                }
            }

        api, client = api_factory(
            [page(1, 2, 800000010), page(2, 2, 800000011)]
        )

        users = list(api.rma.get_rma_details_by_user_id("testuser"))

        assert [u.returns[0].rma_no for u in users] == [800000010, 800000011]
        assert [c[2]["params"].get("pageIndex") for c in client.requests] == [
            None,
            2,
        ]

    def test_api_error_on_a_later_page_is_raised(self, api_factory):
        # The error envelope has to be checked on every page, not just the
        # first one.
        first = {
            "OrderList": {
                "APIPagination": {"pageIndex": 1, "lastIndex": 2},
                "users": [{"userId": "testuser", "returns": []}],
            }
        }
        failure = {
            "OrderList": {
                "APIError": {
                    "Error": [{"errorCode": "SVO_NO_RECORDS"}],
                }
            }
        }

        api, _ = api_factory([first, failure])

        with pytest.raises(ApiError):
            list(api.rma.get_rma_details_by_user_id("testuser"))
