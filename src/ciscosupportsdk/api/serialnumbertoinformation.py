from typing import Iterable

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.serialnumbertoinformation import (
    CoverageOwnerStatus,
    CoverageOwnerStatusResponse,
    CoverageStatus,
    CoverageStatusResponse,
    CoverageSummary,
    CoverageSummaryByInstance,
    CoverageSummaryByInstanceResponse,
    CoverageSummaryResponse,
    OrderableProductList,
    OrderableProductListResponse,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/sn2info/v2"


class SerialNumberToInformationAPI(object):
    """
    The Cisco Serial Number to Information API assists customers and
    partners in identifying an orderable PID and coverage status based
    on a serial number.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("serial_numbers", 75)
    def get_coverage_status(
        self, serial_numbers: list[str]
    ) -> Iterable[CoverageStatus]:
        """
        Returns coverage status for a set of serial numbers.

        :param: serial_numbers: list[str]: Device serial number or
            numbers for which to return results. You can enter up to
            75 serial numbers (each with a maximum length of 40) separated
            by commas.
        :rtype: Iterable[CoverageStatus]
        """
        path = (
            f"{SERVICE_BASE_URL}/coverage/status/serial_numbers/"
            f"{','.join(serial_numbers)}"
        )
        yield from self._session.enumerate_results(
            CoverageStatusResponse, path, paging=False
        )

    @CheckSize("serial_numbers", 75)
    def get_coverage_summary_by_serial(
        self, serial_numbers: list[str]
    ) -> Iterable[CoverageSummary]:
        """
        Returns coverage status, warranty, and product identifier details for
        a set of serial numbers.

        :param: serial_numbers: list[str]: Device serial number or
            numbers for which to return results. You can enter up to
            75 serial numbers (each with a maximum length of 40) separated
            by commas.
        :rtype: Iterable[CoverageSummary]
        """
        path = (
            f"{SERVICE_BASE_URL}/coverage/summary/serial_numbers/"
            f"{','.join(serial_numbers)}"
        )
        yield from self._session.enumerate_results(
            CoverageSummaryResponse, path
        )

    @CheckSize("instance_numbers", 75)
    def get_coverage_summary_by_instance(
        self, instance_numbers: list[str]
    ) -> Iterable[CoverageSummaryByInstance]:
        path = (
            f"{SERVICE_BASE_URL}/coverage/summary/instance_numbers/"
            f"{','.join(instance_numbers)}"
        )
        yield from self._session.enumerate_results(
            CoverageSummaryByInstanceResponse, path
        )

    @CheckSize("serial_numbers", 75)
    def get_orderable_pids(
        self, serial_numbers: list[str]
    ) -> Iterable[OrderableProductList]:
        """
        Returns the orderable PID for the specified device serial number.

        :param: serial_numbers: list[str]: Device serial number or
            numbers for which to return results. You can enter up to
            75 serial numbers (each with a maximum length of 40) separated
            by commas.
        :rtype: Iterable[OrderableProductList]
        """
        path = (
            f"{SERVICE_BASE_URL}/identifiers/orderable/serial_numbers/"
            f"{','.join(serial_numbers)}"
        )
        yield from self._session.enumerate_results(
            OrderableProductListResponse, path, paging=False
        )

    @CheckSize("serial_numbers", 75)
    def get_coverage_owner_status(
        self, serial_numbers: list[str]
    ) -> Iterable[CoverageOwnerStatus]:
        """
        Returns the orderable PID for the specified device serial number.

        :param: serial_numbers: list[str]: Device serial number or
            numbers for which to return results. You can enter up to
            75 serial numbers (each with a maximum length of 40) separated
            by commas.
        :rtype: Iterable[OrderableProductList]
        """
        path = (
            f"{SERVICE_BASE_URL}/coverage/owner_status/serial_numbers/"
            f"{','.join(serial_numbers)}"
        )
        yield from self._session.enumerate_results(
            CoverageOwnerStatusResponse, path, paging=False
        )
