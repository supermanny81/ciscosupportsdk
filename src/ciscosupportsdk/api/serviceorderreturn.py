from typing import Iterable

from ciscosupportsdk.apisession import ApiError, ApiSession
from ciscosupportsdk.models.serviceorderreturn import (
    Rma,
    RmaByUserResponse,
    RmaResponse,
    User,
)

SERVICE_BASE_URL = "/return/v1.0/returns"


class ServiceOrderReturnApi(object):
    """
    The Cisco Service Order Return (RMA) API provides a powerful, convenient,
    and simple way to interact with the Cisco RMA service and enables you to
    access RMA information instantly, programmatically, and in bulk.

    The Cisco Service Order Return (RMA) API is stateless, externally
    accessible, and delivered as a REST web service, which allows you to
    build innovative RMA applications and portals
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    def get_rma_details_by_rma_number(self, rma_number: str) -> Iterable[Rma]:
        """
        Returns detailed information about the specified RMA.

        :param: rma_number: str: Identifier of the RMA for which to
            return details.
            Note: Currently, only one RMA Number is required and accepted.
            In the future, multiple RMA numbers will be supported.
        :rtype: Iterable[Rma]
        """
        path = f"{SERVICE_BASE_URL}/rma_numbers/{rma_number}"
        for _, rmas in self._session.enumerate_results(RmaResponse, path):
            for rma in rmas:
                yield rma

    def get_rma_details_by_user_id(
        self,
        user_id: str,
        from_date: str = None,
        to_date: str = None,
        status: str = None,
        sort_by: str = None,
    ) -> Iterable[User]:
        """
        Returns a list of RMAs associated with the specified user.
        By default, the last 30 days of RMAs for a user is returned.

        :param: user_id: list[str]: Identifier of the user for which
            to return associated RMAs. Note: Only 1 user ID is accepted;
            currently, multiple user IDs are not supported.
        :rtype: Iterable[Rma]
        """
        # TODO: Input validation on query parameter fields.
        path = f"{SERVICE_BASE_URL}/users/user_ids/{user_id}"
        params = {
            "fromDate": from_date,
            "toDate": to_date,
            "status": status,
            "sortBy": sort_by,
        }
        json = self._session._get(path, params)
        if "APIError" in json["OrderList"]:
            raise ApiError(json["OrderList"]["APIError"])
        rma_user_resp = RmaByUserResponse(**json)

        for user in rma_user_resp.order_list.users:
            yield user
        page_data = rma_user_resp.order_list.pagination_response_record
        index = page_data.page_index

        while page_data.page_index < page_data.page_records:
            index += 1
            params["pageIndex"] = index
            json = self._session._get(path, params)
            rma_user_resp = RmaByUserResponse(**json)
            for user in rma_user_resp.order_list.users:
                yield user
