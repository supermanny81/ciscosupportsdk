import time
from typing import Any, Iterable, Optional, Type, TypeVar

from authlib.integrations.requests_client import OAuth2Session
from pydantic import BaseModel, HttpUrl

from ciscosupportsdk.models.common import ApiResponse, CamelCaseApi

ResponseType = TypeVar("ResponseType", bound=ApiResponse)

OAUTH2_URL = "https://id.cisco.com/oauth2/default/v1/token"
BASE_URL = "https://apix.cisco.com"

#: Number of times a throttled (HTTP 429) request is retried before giving up.
MAX_RETRIES = 3
#: Fallback delay, in seconds, when a 429 response carries no Retry-After.
DEFAULT_RETRY_AFTER = 1.0


class ApiError(Exception):
    pass


class RateLimitError(ApiError):
    """
    Raised when the service keeps throttling us after ``MAX_RETRIES``.

    ``retry_after`` carries the value of the last ``Retry-After`` header the
    service sent, when one was present.
    """

    def __init__(self, message: str, retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


class ApiSession(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = BASE_URL,
        token: dict = None,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        """Instances created help manage your API Session.

        Args:
            client_id(basestring): your client id to access the API
            client_secret(basestring): your client secret
            base_url(basestring): service root, overridable for testing
            token(dict): a previously issued token to seed the session with
            max_retries(int): how many times a throttled request is retried
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.token = token if token is not None else {}
        self.client = OAuth2Session(client_id, client_secret, token=self.token)
        self.token = self.client.fetch_token(
            OAUTH2_URL, grant_type="client_credentials"
        )

    def _fetch_token(self) -> None:
        self.token = self.client.fetch_token(
            OAUTH2_URL, grant_type="client_credentials"
        )

    def _check_token(self):
        token = self.client.token
        if not token:
            self._fetch_token()
            return
        # Authlib >= 1.3 exposes ``is_expired`` as a method; older releases
        # exposed it as a property. Reading it without calling it always
        # yields a truthy bound method, which would re-fetch a token before
        # every single request.
        expired = token.is_expired
        if callable(expired):
            expired = expired()
        if expired:
            self._fetch_token()

    def _retry_after(self, response) -> float:
        """Seconds to wait before retrying a throttled request."""
        header = response.headers.get("Retry-After")
        if header is None:
            return DEFAULT_RETRY_AFTER
        try:
            return max(float(header), 0.0)
        except ValueError:
            # Retry-After may also be an HTTP date; we do not try to parse
            # those, the default backoff is good enough.
            return DEFAULT_RETRY_AFTER

    def _request(self, method: str, path: str, **kwargs) -> Any:
        """Sends an HTTP request to the service endpoint.

        Refreshes the token on an expiry-driven 401 and backs off when the
        service throttles us with a 429.
        """
        request_url: HttpUrl = f"{self.base_url}{path}"
        refreshed = False
        # A token refresh does not consume a retry, so allow one extra pass.
        attempts = self.max_retries + 2
        response = None

        for attempt in range(attempts):
            self._check_token()
            response = self.client.request(method, request_url, **kwargs)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 401 and not refreshed:
                # The token was rejected; get a fresh one and try once more.
                refreshed = True
                self._fetch_token()
                continue

            if response.status_code == 429 and attempt < self.max_retries:
                time.sleep(self._retry_after(response))
                continue

            msg: str = f"{response.status_code}: {response.content}"
            if response.status_code == 429:
                raise RateLimitError(msg, self._retry_after(response))
            raise ApiError(msg)

        # Unreachable as written: the 401 retry is latched by ``refreshed``
        # and the 429 retry stops at ``max_retries``, both of which are below
        # ``attempts``, so the loop always returns or raises. Kept so that a
        # future change to those conditions cannot make this method fall out
        # and silently return None.
        msg = f"{response.status_code}: {response.content}"  # pragma: nocover
        if response.status_code == 429:  # pragma: nocover
            raise RateLimitError(msg, self._retry_after(response))
        raise ApiError(msg)  # pragma: nocover

    def _get(self, path: str, params: dict) -> Any:
        """Sends an HTTP get request to the service endpoint."""
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: dict = None, params: dict = None) -> Any:
        """Sends an HTTP post request to the service endpoint.

        The Automated Software Distribution API takes its inputs as a JSON
        request body rather than as path or query parameters.
        """
        return self._request("POST", path, json=json, params=params)

    def get_result(
        self,
        response_type: Type[ResponseType],
        path: str,
        query_params: dict = None,
    ) -> BaseModel:
        """
        Used when an API response returns a single object and there is
        no need to use a generator.
        """
        # get the response, return the items
        json = self._get(path, dict(query_params or {}))
        response = response_type(**json)
        return response.items

    def enumerate_results(
        self,
        response_type: Type[ResponseType],
        path: str,
        query_params: dict = None,
        page_index: int = 1,
        paging: bool = True,
    ) -> Iterable[BaseModel]:
        """
        Used when an API response returns a list of objects.

        This method is a generator in support pagination of
        potentially large amounts of data to process.
        """
        # copy so the caller's dict is never mutated and page state cannot
        # leak between unrelated calls
        query_params = dict(query_params or {})
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

        if not paging:
            return

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
