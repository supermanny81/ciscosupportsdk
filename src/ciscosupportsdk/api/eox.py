from datetime import date, datetime
from typing import Iterable, Union

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.eox import (
    EoxAttrib,
    EoxRecord,
    EoxResponse,
    SoftwareRelease,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/supporttools/eox/rest/5"


class EoxError(Exception):
    """
    Server side errors in processing the request throw an EoxError.

    If you see one of these, make sure to look at the message body
    to see why the error occurred.
    """

    pass


class EoxApi(object):
    """
    The Cisco EoX API provides access to Cisco End of Life product data.

    Using the EoX Service API, customers and partners can request Cisco
    EoX product information for both hardware and software using a variety
    of input mechanisms.
    """

    _default_params = {"responseencoding": "json"}

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("eox_attribs", 20)
    def get_by_dates(
        self,
        start_date: Union[str, datetime.date],
        end_date: Union[str, datetime.date],
        eox_attribs: list[EoxAttrib],
    ) -> Iterable[EoxRecord]:
        """
        Get EoX notices for all products by date.

        Returns all active and inactive EoX records for all products with the
        specified eoxAttrib value within an inclusive date range. If you do
        not specify an eoxAttrib value, this method returns records with an
        updated time stamp within the specified date range.

        Note: This method can be used to retrieve records based on any date
        listed in the EoX record. For example, if you specify a date range
        and enter EO_SALE_DATE and EO_LAST_SUPPORT_DATE as the eoxAttrib
        values, this method returns records with an end of sale date or last
        date of support within the specified date range. This feature allows
        you to target specific date ranges within each attribute without having
        to pull the entire database.

        Args:
            start_date: Start date of the date range of records to
                return in the following format: YYYY-MM-DD.
                For example: 2010-01-01
            end_date: End date of the date range of records to return
                in the following format: YYYY-MM-DD. For example: 2010-01-01
        Returns:
            Iterable[EoxRecord]
        Raises:
            EoxError, ValueError: Depending on errors with input or processing
            the request on the server.
        """
        params = {"eoxAttrib": ",".join(eox_attribs)}

        yield from self._enumerate_results(
            "EOXByDates",
            [self._get_date(start_date), self._get_date(end_date)],
            params,
        )

    @CheckSize("product_ids", 20)
    def get_by_product_ids(
        self, product_ids: list[str]
    ) -> Iterable[EoxRecord]:
        _product_ids = ",".join(product_ids)
        """
        Get EoX records by product ID.

        Returns one or more EOX records for the product or products
        with the specified product ID (PID) or product IDs.

        Args:
            product_ids: Product IDs for the products
                to retrieve from the database. Enter up to 20 PIDs
                separated by commas.

                For example: 15216-OADM1-35=,M92S1K9-1.3.3C Note: To
                enhance search capabilities, the Cisco Support Tools
                allows wildcards with the productIDs parameter. A
                minimum of 3 characters is required. For example, only
                the following inputs are valid: *VPN*, *VPN, VPN*, and
                VPN. Using wildcards can result in multiple PIDs in the
                output.
        Returns:
            Iterable[EoxRecord]
        Raises:
            EoxError, ValueError
        """
        yield from self._enumerate_results("EOXByProductID", [_product_ids])

    @CheckSize("serial_numbers", 20)
    def get_by_serial_number(
        self, serial_numbers: list[str]
    ) -> Iterable[EoxRecord]:
        """
        Returns the EoX record for products with the specified serial numbers.

        Args:
            serial_numbers: Device serial number or numbers
                for which to return results. You can enter up to 20 serial
                numbers (each with a maximum length of 40) separated by commas.
        Returns:
            Iterable[EoxRecord]
        Raises:
            EoxError, ValueError
        """
        _serial_numbers = ",".join(serial_numbers)
        yield from self._enumerate_results(
            "EOXBySerialNumber", [_serial_numbers]
        )

    @CheckSize("software_releases", 20)
    def get_by_software_release(
        self, software_releases: list[SoftwareRelease]
    ) -> Iterable[EoxRecord]:
        """
        Returns the EoX record for products associated with the specified
        software release and (optionally) the specified operating system.

        Args:
            software_release: A combination of
                software release and operating system.  Up to 20 combinations
                may be used and each may return multiple entires.
        Returns:
            Iterable[EoxRecord]
        Raises:
            EoxError, ValueError
        """
        _software_releases = {}
        for count, value in enumerate(software_releases):
            _software_releases[f"input{count + 1}"] = str(value)

        yield from self._enumerate_results(
            "EOXBySWReleaseString", [], _software_releases
        )

    def _enumerate_results(
        self,
        endpoint: str,
        path_params: list,
        params: dict = {},
        page_index: int = 1,
    ) -> Iterable[EoxRecord]:
        """
        Overload the default method for pagination.

        The EoX API behaves differently.  Pagination responses, urls,
        and errors.
        """
        path = (
            f"{SERVICE_BASE_URL}/{endpoint}/{page_index}/"
            f"{'/'.join(x for x in path_params)}"
        )
        json = self._session._get(path, {**self._default_params, **params})

        if "EOXError" in json:  # check for errors
            raise EoxError(json["EOXError"])
        else:
            response = EoxResponse(**json)
            # break out the response into paging and EoX data
            eox_records, pagination_response = (
                response.eox_record,
                response.pagination_response_record,
            )
            for record in eox_records:
                yield record
            # if there are more pages, iterate through the next one
            if pagination_response.page_index < pagination_response.last_index:
                page_index += 1
                yield from self._enumerate_results(
                    endpoint, path_params, params, page_index
                )

    def _get_date(self, d: Union[str, datetime.date]) -> str:
        return d.strftime("%Y-%m-%d") if isinstance(d, date) else d
