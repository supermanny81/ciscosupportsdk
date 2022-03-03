from typing import Iterable, Type, TypeVar

from authlib.integrations.requests_client import OAuth2Session
from pydantic import BaseModel, HttpUrl

from ciscosupportsdk.models.common import ApiResponse, CamelCaseApi

ResponseType = TypeVar("ResponseType", bound=ApiResponse)

OAUTH2_URL = "https://cloudsso.cisco.com/as/token.oauth2"
BASE_URL = "https://api.cisco.com"


class ApiError(Exception):
    pass


class ApiSession(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = BASE_URL,
        token: dict = {},
    ) -> None:
        """Instances created help manage your API Session.

        Args:
            client_id(basestring): your client id to access the API
        """
        self.token = token
        self.client = OAuth2Session(client_id, client_secret, token=self.token)
        self.token = self.client.fetch_token(
            OAUTH2_URL, grant_type="client_credentials"
        )

    def _check_token(self):
        if self.client.token.is_expired:
            self.token = self.client.fetch_token(
                OAUTH2_URL, grant_type="client_credentials"
            )

    def _get(self, path: str, params: dict) -> str:
        """Sends an HTTP get request to the service endpoint."""
        request_url: HttpUrl = f"{BASE_URL}{path}"
        # check and refresh the token if needed
        self._check_token()
        response = self.client.get(request_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            # TODO: handle rate limiting requests
            msg: str = f"{response.status_code}: {response.content}"
            raise ApiError(msg)

    def get_result(
        self,
        response_type: Type[ResponseType],
        path: str,
        query_params: dict = {},
    ) -> BaseModel:
        """
        Used when an API response returns a single object and there is
        no need to use a generator.
        """
        # get the response, return the items
        json = self._get(path, query_params)
        response = response_type(**json)
        return response.items

    def enumerate_results(
        self,
        response_type: Type[ResponseType],
        path: str,
        query_params: dict = {},
        page_index: int = 1,
        paging: bool = True,
    ) -> Iterable[BaseModel]:
        """
        Used when an API response returns a list of objects.

        This method is a generator in support pagination of
        potentially large amounts of data to process.
        """
        if issubclass(response_type, CamelCaseApi):
            query_params["pageIndex"] = page_index
        else:
            query_params["page_index"] = page_index

        # get the response, return the items
        json = self._get(path, query_params)
        if "APIError" in json:  # houston, we have a problem!
            raise ApiError(json)

        response = response_type(**json)
        for item in response.items:
            yield item

        # handle pagination, if needed
        if hasattr(response, "pagination_response_record"):
            pages = response.pagination_response_record
            if pages is not None:
                # if there are more pages, iterate through them as well
                if pages.page_index < pages.last_index:
                    page_index += 1
                    yield from self.enumerate_results(
                        response_type, path, query_params, page_index
                    )
