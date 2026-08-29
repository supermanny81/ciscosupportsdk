from fixtures import *  # noqa

from ciscosupportsdk.models.serialnumbertoinformation import CoverageStatus


class TestSerialNumberToInfoApi:
    def test_get_coverage_status(self, api_factory):
        api, client = api_factory("sn_to_info/get_coverage_status")

        status: CoverageStatus = next(
            api.serial_information.get_coverage_status(["SAL1234ABCD"])
        )

        assert status.serial_number == "SAL1234ABCD"
        assert status.is_covered is True
        assert status.coverage_end_date == "2023-12-31"
        # SN2INFO is a snake_case API; it must not be sent pageIndex.
        assert client.params() == {"page_index": 1}

    def test_get_coverage_summary_by_serial(self, api_factory):
        api, _ = api_factory("sn_to_info/get_coverage_summary_by_serial")

        summaries = list(
            api.serial_information.get_coverage_summary_by_serial(
                ["SAL1234ABCD"]
            )
        )

        assert len(summaries) == 1
        assert summaries[0].base_pid_list[0].base_pid
        assert summaries[0].orderable_pid_list

    def test_get_orderable_pids(self, api_factory):
        api, client = api_factory("sn_to_info/get_orderable_pids")

        results = list(
            api.serial_information.get_orderable_pids(
                ["FOC1111AAAA", "FOC2222BBBB", "FOC3333CCCC"]
            )
        )

        assert len(results) == 3
        assert results[0].orderable_pid_list[0].pillar_description
        assert "FOC1111AAAA,FOC2222BBBB,FOC3333CCCC" in client.urls[0]

    def test_get_coverage_owner_status(self, api_factory):
        api, _ = api_factory("sn_to_info/get_coverage_owner_status")

        results = list(
            api.serial_information.get_coverage_owner_status(["SAL1234ABCD"])
        )

        assert len(results) == 1
        assert results[0].is_owner is True

    def test_uncovered_serial_omits_contract_fields(self, api_factory):
        # Contract, warranty and site data are simply absent when a serial
        # is not covered -- this is the shape that used to raise.
        api, _ = api_factory(
            {"serial_numbers": [{"sr_no": "SAL0000NONE", "is_covered": "NO"}]}
        )

        status = next(
            api.serial_information.get_coverage_status(["SAL0000NONE"])
        )

        assert status.is_covered is False
        assert status.coverage_end_date is None

    def test_get_coverage_summary_by_instance(self, api_factory):
        # Previously unskippable: it needed a live instance number. The
        # instance endpoint is the only one that returns a postal code.
        api, client = api_factory(
            {
                "pagination_response_record": {
                    "last_index": 1,
                    "page_index": 1,
                    "page_records": 1,
                    "total_records": 1,
                },
                "instance_numbers": [
                    {
                        "id": "1",
                        "instance_number": "917582445",
                        "parent_instance_no": "917582440",
                        "sr_no": "SAL1234ABCD",
                        "is_covered": "YES",
                        "base_pid": {"base_pid": "C9410R"},
                        "orderable_pid": {
                            "item_description": "Catalyst 9400 chassis",
                            "item_position": "P",
                            "item_type": "CHASSIS",
                            "orderable_pid": "C9410R",
                        },
                        "contract_site_postal_code": "95134",
                        "contract_site_city": "EXAMPLE CITY",
                    }
                ],
            }
        )

        results = list(
            api.serial_information.get_coverage_summary_by_instance(
                ["917582445"]
            )
        )

        assert len(results) == 1
        assert results[0].instance_number == "917582445"
        assert results[0].contract_site_postal_code == "95134"
        assert results[0].base_pid.base_pid == "C9410R"
        assert "/coverage/summary/instance_numbers/917582445" in client.urls[0]
