from typing import Iterable

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.case import (
    Case,
    CaseDetail,
    CaseDetailResponse,
    CaseResponse,
    CaseStatusFlag,
    CaseSummaryResponse,
    SortCaseBy,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/case/v3/cases"


class CaseApi(object):
    """
    The Cisco Support Case API v3 provides a powerful, convenient, and simple
    way to interact with the Cisco Support Case Manager tool and aims to
    improve the partner and customer experience by enabling you to access case
    information instantly, programmatically, and in bulk.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("case_ids", 30)
    def get_case_summary(
        self,
        case_ids: list[str],
        sort_by: SortCaseBy = SortCaseBy.UPDATED_DATE,
    ) -> Iterable[Case]:
        """
        Returns brief information for the specified case or cases.

        :param: case_ids: list[str]: Identifier of the case or cases for which
            to return results. Multiple values must be specified within a
            comma-separated list and cannot exceed 30 IDs.
        :param: sort_by: SortCaseBy: Order in which the results should be
            sorted.
        """
        path = f"{SERVICE_BASE_URL}/case_ids/" f"{','.join(case_ids)}"
        params = {"sort_by": sort_by}

        yield from self._session.enumerate_results(
            CaseSummaryResponse, path, query_params=params
        )

    def get_case_details(self, case_id: str) -> CaseDetail:
        """
        Returns detailed information for the specified case.

        :param: case_id: str: Identifier of the case for which to return
            results.
        """
        path = f"{SERVICE_BASE_URL}/details/case_id/{case_id}"
        return self._session.get_result(CaseDetailResponse, path)

    @CheckSize("contract_ids", 10)
    def get_cases_by_contract_id(
        self,
        contract_ids: list[str],
        date_created_from: str = None,
        date_created_to: str = None,
        status_flag: CaseStatusFlag = CaseStatusFlag.OPEN,
    ) -> Iterable[Case]:
        """
        Returns summary information for cases associated with the specified
        contract or contracts.

        :param: contract_ids: list[str]: Identifier of the user or users for
            which to return results.  A maximum of 10 may be passed.
        :param: date_created_from: str: Beginning date (in UTC) of the range
            in which to search. For example: 2013-04-23T11:00:14Z
            Note: The maximum date range currently supported is 90 days.
        :param: date_created_to: str: End date (in UTC) of the range
            in which to search. For example: 2013-04-23T11:00:14Z
            Note: The maximum date range currently supported is 90 days.
        :param: status_flag: CaseStatusFlag: Return only cases associated
            with the specified status.
        """
        path = (
            f"{SERVICE_BASE_URL}/contracts/contract_ids/"
            f"{','.join(contract_ids)}"
        )
        params = {
            "date_created_from": date_created_from,
            "date_created_to": date_created_to,
            "status_flag": status_flag,
        }
        yield from self._session.enumerate_results(
            CaseResponse, path, query_params=params
        )

    @CheckSize("user_ids", 10)
    def get_cases_by_user_id(
        self,
        user_ids: list[str],
        date_created_from: str = None,
        date_created_to: str = None,
        status_flag: CaseStatusFlag = CaseStatusFlag.OPEN,
    ) -> Iterable[Case]:
        """
        Returns summary information for cases associated with the specified
        contract or contracts.

        :param: user_ids: list[str]: Identifier of the user or users for
            which to return results.  A maximum of 10 may be passed.
        :param: date_created_from: str: Beginning date (in UTC) of the range
            in which to search. For example: 2013-04-23T11:00:14Z
            Note: The maximum date range currently supported is 90 days.
        :param: date_created_to: str: End date (in UTC) of the range
            in which to search. For example: 2013-04-23T11:00:14Z
            Note: The maximum date range currently supported is 90 days.
        :param: status_flag: CaseStatusFlag: Return only cases associated
            with the specified status.
        """
        path = f"{SERVICE_BASE_URL}/users/user_ids/" f"{','.join(user_ids)}"
        params = {
            "date_created_from": date_created_from,
            "date_created_to": date_created_to,
            "status_flag": status_flag,
        }
        yield from self._session.enumerate_results(
            CaseResponse, path, query_params=params
        )
