"""
The Cisco Support APIs omit empty and null fields from their responses rather
than sending them as nulls. Every model must therefore validate a payload that
carries only the identifying field, otherwise perfectly ordinary responses
raise ValidationError.
"""

import importlib
import pkgutil

from pydantic import BaseModel

from ciscosupportsdk.models.bug import ListOfBugs, Severity, SortBy
from ciscosupportsdk.models.case import CaseStatusFlag
from ciscosupportsdk.models.common import PaginationResponseRecord
from ciscosupportsdk.models.eox import EoxResponse
from ciscosupportsdk.models.productinformation import (
    ProductInformationResponse,
)
from ciscosupportsdk.models.serialnumbertoinformation import (
    CoverageSummaryByInstanceResponse,
    CoverageSummaryResponse,
)
from ciscosupportsdk.models.serviceorderreturn import RmaResponse
from ciscosupportsdk.models.softwaresuggestion import (
    CompatableSoftwareResponse,
    SuggestionsByProductResponse,
)


def _model_modules(package):
    """Every module under ciscosupportsdk.models."""
    for info in pkgutil.iter_modules(package.__path__):
        yield importlib.import_module(f"{package.__name__}.{info.name}")


class TestSparsePayloads:
    def test_rma_without_labor_or_tracking(self):
        # Labor details only exist for onsite service and tracking only once
        # a part has shipped, so a closed, parts-only RMA omits both.
        payload = {
            "returns": {
                "RmaRecord": [
                    {"rmaNo": 800000001, "status": "Closed"},
                ]
            }
        }

        rma = RmaResponse(**payload).items.rma_records[0]

        assert rma.rma_no == 800000001
        assert rma.labor_details is None
        assert rma.replacement_parts is None
        assert rma.ship_to_info is None

    def test_coverage_summary_for_uncovered_serial(self):
        # Contract, warranty and site fields are absent when is_covered is NO.
        payload = {
            "serial_numbers": [{"sr_no": "SAL1234ABCD", "is_covered": "NO"}]
        }

        coverage = CoverageSummaryResponse(**payload).items[0]

        assert coverage.sr_no == "SAL1234ABCD"
        assert coverage.is_covered is False
        assert coverage.service_contract_number is None
        # Collections stay iterable.
        assert coverage.base_pid_list == []
        assert coverage.orderable_pid_list == []

    def test_coverage_summary_by_instance_carries_postal_code(self):
        # contract_site_postal_code is documented on the instance endpoint
        # only; it used to be dropped on the floor.
        payload = {
            "instance_numbers": [
                {
                    "instance_number": "917582445",
                    "contract_site_postal_code": "95134",
                }
            ]
        }

        coverage = CoverageSummaryByInstanceResponse(**payload).items[0]

        assert coverage.instance_number == "917582445"
        assert coverage.contract_site_postal_code == "95134"

    def test_eox_record_without_migration_details(self):
        # Products with no migration path omit the whole block.
        payload = {
            "PaginationResponseRecord": {
                "PageIndex": 1,
                "LastIndex": 1,
                "TotalRecords": 1,
                "PageRecords": 1,
            },
            "EOXRecord": [
                {
                    "EOLProductID": "WS-C3560-48PS-S",
                    "EndOfSaleDate": {"value": "2015-01-30"},
                }
            ],
        }

        record = EoxResponse(**payload).eox_record[0]

        assert record.eol_product_id == "WS-C3560-48PS-S"
        assert record.eox_migration_details is None
        assert record.last_date_of_support is None

    def test_eox_empty_date_falls_back(self):
        payload = {"EOXRecord": [{"EndOfSaleDate": {"value": ""}}]}

        record = EoxResponse(**payload).eox_record[0]

        assert record.end_of_sale_date.to_date().year == 2099

    def test_product_information_keeps_serial_and_pids(self):
        # sr_no, base_pid and orderable_pid are returned by the by-serial
        # endpoint and are the only way to correlate a record with its input.
        payload = {
            "product_list": [
                {
                    "sr_no": "SAL1234ABCD",
                    "base_pid": "WS-C3560-48PS-S",
                    "orderable_pid": "WS-C3560-48PS-S=",
                    "product_name": "Catalyst 3560 48 Port",
                }
            ]
        }

        record = ProductInformationResponse(**payload).items[0]

        assert record.sr_no == "SAL1234ABCD"
        assert record.base_pid == "WS-C3560-48PS-S"
        assert record.orderable_pid == "WS-C3560-48PS-S="
        # Hardware-only fields the API omits.
        assert record.dimensions is None
        assert record.weight is None

    def test_software_suggestion_without_error_block(self):
        # errorDetailsResponse is only present when a lookup failed. It used
        # to be declared required, which rejected every successful response.
        payload = {
            "status": "Success",
            "productList": [
                {
                    "id": "1",
                    "product": {"basePID": "WS-C3560-48PS-S"},
                    "suggestions": [{"id": "1", "releaseFormat1": "15.0(2)"}],
                }
            ],
        }

        response = SuggestionsByProductResponse(**payload)

        assert response.error_details_response is None
        suggestion = response.items[0].suggestions[0]
        assert suggestion.release_format1 == "15.0(2)"
        assert suggestion.error_details_response is None
        assert suggestion.images == []

    def test_compatible_software_without_error_block(self):
        response = CompatableSoftwareResponse(
            **{"status": "Success", "suggestions": [{"id": "1"}]}
        )

        assert response.error_details_response is None
        assert response.items[0].id == "1"

    def test_bug_with_only_an_id(self):
        bug = ListOfBugs(**{"bugs": [{"bug_id": "CSCvc57217"}]}).items[0]

        assert bug.bug_id == "CSCvc57217"
        assert bug.headline is None
        assert bug.support_case_count is None


class TestPrintableEnum:
    def test_str_returns_the_wire_value(self):
        # Enums are interpolated straight into query strings, so __str__ has
        # to yield the API's value rather than "Severity.ONE".
        assert str(Severity.ONE) == "1"
        assert str(SortBy.SEVERITY) == "severity"
        assert str(CaseStatusFlag.OPEN) == "O"


class TestPaginationResponseRecord:
    """
    Regression cover for the two reported issues:
    sparse pagination blocks and population by field name.
    """

    def test_sparse_block_validates(self):
        # A zero-record response omits most of the block. This used to raise
        # ValidationError mid-generator, which callers could only tell apart
        # from a malformed response by string-matching the exception.
        record = PaginationResponseRecord(
            **{"last_index": 1, "page_index": 1, "total_records": 0}
        )

        assert record.total_records == 0
        assert record.page_records is None
        assert record.self_link is None

    def test_entirely_absent_block_validates(self):
        record = PaginationResponseRecord()

        # Defaulting the indices to 1 rather than None keeps a missing block
        # meaning "one page of results", so the pagination comparison in
        # ApiSession.enumerate_results stays a valid int comparison.
        assert record.page_index == 1
        assert record.last_index == 1

    def test_populates_by_alias(self):
        record = PaginationResponseRecord(
            title="t",
            pageIndex=2,
            lastIndex=3,
            totalRecords=30,
            pageRecords=10,
            selfLink="https://example.invalid",
        )

        assert (record.page_index, record.last_index) == (2, 3)

    def test_populates_by_field_name(self):
        # populate_by_name was configured through a v1 class-based Config,
        # which pydantic v2 leaves inert -- so this raised ValidationError
        # despite the config claiming otherwise.
        record = PaginationResponseRecord(
            title="t",
            page_index=2,
            last_index=3,
            total_records=30,
            page_records=10,
            self_link="https://example.invalid",
        )

        assert (record.page_index, record.last_index) == (2, 3)


class TestPydanticV2Compatibility:
    def test_no_class_based_config_remains(self):
        # Class-based Config is inert under v2 and removed in v3; every model
        # must use model_config instead.
        import ciscosupportsdk.models as models

        offenders = []
        for module in _model_modules(models):
            for obj in vars(module).values():
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    if "Config" in vars(obj):
                        offenders.append(f"{module.__name__}.{obj.__name__}")

        assert offenders == []

    def test_yes_no_strings_still_coerce_to_bool(self):
        # The APIs send "YES"/"NO" rather than booleans; v2's coercion rules
        # differ from v1's, so this is worth pinning.
        payload = {"serial_numbers": [{"sr_no": "X", "is_covered": "NO"}]}

        assert CoverageSummaryResponse(**payload).items[0].is_covered is False
