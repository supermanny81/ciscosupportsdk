from typing import Iterable

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.bug import (
    Bug,
    DateModified,
    ListOfBugs,
    Severity,
    SortBy,
    Status,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/bug/v2.0/bugs"


class BugApi(object):
    """
    Cisco defects (or bugs) are made visible to customers and partners through
    the use of the Bug Search Tool (BST) application. The objective of the
    Cisco Bug API is to provide an entry point into the Bug Search Tool for
    customers and partners to view bug details and perform bug searches while
    integrating the search results into their own interfaces and applications.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("bug_ids", 5)
    def get_bug_details(self, bug_ids: list[str]) -> Iterable[Bug]:
        """
        Returns detailed information for the specified bug ID or IDs.

        :param: bug_ids: list[str]: Identifier of the bug or bugs for which
            to return detailed information. A maximum of five (5) bug IDs can
            be submitted separated by a comma.
        :rtype: Bug
        """
        path = f"{SERVICE_BASE_URL}/bug_ids/" f"{','.join(bug_ids)}"
        yield from self._session.enumerate_results(
            ListOfBugs, path, paging=False
        )

    def get_bugs_by_product_id(
        self,
        base_pid: str,
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the
        specified base product ID.

        :param: base_pid: str: Identifier of the base product for which to
            return details on associated bugs. Only one base product ID can
            be submitted.
        :param: status: Status: Status of the bug; only bugs with the
            specified status are returned.
        :param: modified_date: DateModified: Last modified date of the bug;
            only bugs modified within the specified time are returned.
        :param: severity: Severity: Severity of the bug; only bugs with
            the specified severity are returned.
        :param: sort_by: SortBy: Parameter on which to sort the results.
        :rtype: ProductBug
        """
        path = f"{SERVICE_BASE_URL}/products/product_id/{base_pid}"
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    @CheckSize("software_releases", 75)
    def get_bugs_by_product_id_and_release(
        self,
        base_pid: str,
        software_releases: list[str],
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the
        specified base product ID.

        :param: base_pid: str: Identifier of the base product for which to
            return details on associated bugs. Only one base product ID can
            be submitted.
        :param: status: Status: Status of the bug; only bugs with the
            specified status are returned.
        :param: modified_date: DateModified: Last modified date of the bug;
            only bugs modified within the specified time are returned.
        :param: severity: Severity: Severity of the bug; only bugs with
            the specified severity are returned.
        :param: sort_by: SortBy: Parameter on which to sort the results.
        :rtype: ProductBug
        """
        path = (
            f"{SERVICE_BASE_URL}/products/product_id/{base_pid}"
            f"/software_releases/{','.join(software_releases)}"
        )
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    def get_bugs_by_keyword(
        self,
        keyword: str,
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the
        specified keyword.

        :param: keyword: str: Keyword or keywords for which to return details
            on associated bugs. Multiple words can be submitted
        :param: status: Status: Status of the bug; only bugs with the
            specified status are returned.
        :param: modified_date: DateModified: Last modified date of the bug;
            only bugs modified within the specified time are returned.
        :param: severity: Severity: Severity of the bug; only bugs with
            the specified severity are returned.
        :param: sort_by: SortBy: Parameter on which to sort the results.
        :rtype: ProductBug
        """
        path = f"{SERVICE_BASE_URL}/keyword/{keyword}"
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    @CheckSize("affected_releases", 75)
    def get_bugs_by_product_and_affected_release(
        self,
        product_series: str,
        affected_releases: list[str],
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the specified
        hardware product series and affected software release or releases.
        """
        path = (
            f"{SERVICE_BASE_URL}/product_series/{product_series}"
            f"/affected_releases/{','.join(affected_releases)}"
        )
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    @CheckSize("fixed_in_releases", 75)
    def get_bugs_by_product_and_fixed_release(
        self,
        product_series: str,
        fixed_in_releases: list[str],
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the specified
        hardware product series and affected software release or releases.
        """
        path = (
            f"{SERVICE_BASE_URL}/product_series/{product_series}"
            f"/fixed_in_releases/{','.join(fixed_in_releases)}"
        )
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    @CheckSize("affected_releases", 75)
    def get_bugs_by_product_name_and_affected_release(
        self,
        product_name: str,
        affected_releases: list[str],
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the
        specified product name and affected software release or releases.
        """
        path = (
            f"{SERVICE_BASE_URL}/product_name/{product_name}"
            f"/affected_releases/{','.join(affected_releases)}"
        )
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )

    @CheckSize("fixed_in_releases", 75)
    def get_bugs_by_product_name_and_fixed_release(
        self,
        product_name: str,
        fixed_in_releases: list[str],
        status: Status = None,
        modified_date: DateModified = None,
        severity: Severity = None,
        sort_by: SortBy = None,
    ) -> Iterable[Bug]:
        """
        Returns detailed information for the bugs associated with the
        specified product name and affected software release or releases.
        """
        path = (
            f"{SERVICE_BASE_URL}/product_name/{product_name}"
            f"/fixed_in_releases/{','.join(fixed_in_releases)}"
        )
        params = {
            "status": status,
            "modified_date": modified_date,
            "severity": severity,
            "sort_by": sort_by,
        }
        yield from self._session.enumerate_results(
            ListOfBugs, path, params, paging=True
        )
