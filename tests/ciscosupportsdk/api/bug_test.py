from fixtures import *  # noqa

from ciscosupportsdk.models.bug import Bug, DateModified, SortBy


class TestBugApi:
    def test_get_bug_details(self, api_factory):
        api, client = api_factory("bug/get_bug_details")

        details: Bug = next(api.bug.get_bug_details(["CSCvc57217"]))

        assert details.bug_id == "CSCvc57217"
        assert details.base_pid is None
        assert client.urls[0].endswith("/bug/v2.0/bugs/bug_ids/CSCvc57217")

    def test_get_bugs_by_product_id(self, api_factory):
        api, client = api_factory("bug/get_bugs_by_product_id")

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_id(
                "WS-C3560-48PS-S", sort_by=SortBy.SEVERITY
            )
        )

        assert count == 3
        assert client.params()["sort_by"] == SortBy.SEVERITY

    def test_get_bugs_by_product_id_and_release(self, api_factory):
        api, _ = api_factory("bug/get_bugs_by_product_id_and_release")

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_id_and_release(
                "WS-C3560-48PS-S", ["15.2(03)E01"]
            )
        )

        assert count == 0

    def test_get_bugs_by_keyword(self, api_factory):
        api, client = api_factory("bug/get_bugs_by_keyword")

        count = sum(1 for _ in api.bug.get_bugs_by_keyword("IOS SSH PKI"))

        assert count == 3
        assert "/bugs/keyword/IOS SSH PKI" in client.urls[0]

    def test_get_bugs_by_product_and_affected_release(self, api_factory):
        api, _ = api_factory("bug/get_bugs_by_product_and_affected_release")

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_and_affected_release(
                "Cisco 5500 Series Wireless Controllers",
                ["7.4(100.0)"],
                modified_date=DateModified.ALL,
            )
        )

        assert count == 0

    def test_get_bugs_by_product_and_fixed_release(self, api_factory):
        api, _ = api_factory("bug/get_bugs_by_product_and_fixed_release")

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_and_fixed_release(
                "Cisco 5500 Series Wireless Controllers",
                ["7.6(100.6)"],
                modified_date=DateModified.ALL,
            )
        )

        assert count == 0

    def test_get_bugs_by_product_name_and_affected_release(self, api_factory):
        # Three pages of results; the SDK must follow pagination to the end.
        api, client = api_factory(
            "bug/get_bugs_by_product_name_and_affected_release"
        )

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_name_and_affected_release(
                "Cisco Unity Connection Version 10.5",
                ["10.5(2)"],
                modified_date=DateModified.ALL,
            )
        )

        assert count == 9
        assert [c[2]["params"]["page_index"] for c in client.requests] == [
            1,
            2,
            3,
        ]

    def test_get_bugs_by_product_name_and_fixed_release(self, api_factory):
        api, _ = api_factory("bug/get_bugs_by_product_name_and_fixed_release")

        count = sum(
            1
            for _ in api.bug.get_bugs_by_product_name_and_fixed_release(
                "Cisco Unified Communications Manager (CallManager)",
                ["10.5(2)"],
                modified_date=DateModified.ALL,
            )
        )

        assert count == 0
