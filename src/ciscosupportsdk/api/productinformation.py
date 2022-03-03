from typing import Iterable

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.productinformation import (
    ProductInformationRecord,
    ProductInformationResponse,
    ProductMDFRecord,
    ProductMDFResponse,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/product/v1/information"


class ProductInformationApi(object):
    """
    The Cisco Product Information API looks up details on products using serial
    numbers and product IDs.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("serial_numbers", 5)
    def get_info_by_serial(
        self, serial_numbers: list[str]
    ) -> Iterable[ProductInformationRecord]:
        """
        Returns product information associated with the specified serial ]
        number or numbers.
        """
        path = (
            f"{SERVICE_BASE_URL}/serial_numbers/" f"{','.join(serial_numbers)}"
        )
        yield from self._session.enumerate_results(
            ProductInformationResponse, path
        )

    @CheckSize("product_ids", 5)
    def get_info_by_product_id(
        self, product_ids: list[str]
    ) -> Iterable[ProductInformationRecord]:
        """
        Returns product information associated with the specified product
        identifier or identifiers.
        """
        path = f"{SERVICE_BASE_URL}/product_ids/" f"{','.join(product_ids)}"
        yield from self._session.enumerate_results(
            ProductInformationResponse, path
        )

    @CheckSize("product_ids", 5)
    def get_mdf_by_product_id(
        self, product_ids: list[str]
    ) -> Iterable[ProductMDFRecord]:
        """
        Returns metadata framework (MDF) identifiers associated with
        the specified product identifier or identifiers.Returns metadata
        framework (MDF) identifiers associated with the specified product
        identifier or identifiers.
        """
        path = (
            f"{SERVICE_BASE_URL}/product_ids_mdf/" f"{','.join(product_ids)}"
        )
        yield from self._session.enumerate_results(ProductMDFResponse, path)
