from typing import Iterable

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.softwaresuggestion import (
    CompatableSoftwareResponse,
    Suggestion,
    Suggestions,
    SuggestionsByProductResponse,
)
from ciscosupportsdk.validate import CheckSize

SERVICE_BASE_URL = "/software/suggestion/v2/suggestions"


class SoftwareSuggestionApi(object):
    """
    The process of selecting the appropriate software upgrade path for your
    environment can be complex. The Cisco Software Suggestions streamline the
    software selection process by providing the necessary information to assist
    you in making intelligent choices for upgrading your software.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    @CheckSize("product_ids", 10)
    def get_suggestions_and_image_by_product_ids(
        self, product_ids: list[str]
    ) -> Iterable[Suggestions]:
        """
        Returns a list of Cisco suggested software releases and images for a
        list of product IDs.

        :param: product_ids: list[str]: Base product IDs for which to return
            suggested software releases. A maximum of 10 PIDs are allowed.
        """
        path = (
            f"{SERVICE_BASE_URL}/software/productIds/"
            f"{','.join(product_ids)}"
        )
        yield from self._session.enumerate_results(
            SuggestionsByProductResponse, path
        )

    @CheckSize("product_ids", 10)
    def get_suggestions_by_product_ids(
        self, product_ids: list[str]
    ) -> Iterable[Suggestions]:
        """
        Returns a list of Cisco suggested software releases (without images)
        for a list of product IDs.

        :param: product_ids: list[str]: Base product IDs for which to return
            suggested software releases. A maximum of 10 PIDs are allowed.
        """
        path = (
            f"{SERVICE_BASE_URL}/releases/productIds/"
            f"{','.join(product_ids)}"
        )
        yield from self._session.enumerate_results(
            SuggestionsByProductResponse, path
        )

    def get_compatible_by_product_id(
        self,
        product_id: str,
        current_image: str = None,
        current_release: str = None,
        supported_features: list[str] = None,
        supported_hardware: list[str] = None,
    ) -> Iterable[Suggestion]:
        """
        Returns compatible and suggested software releases for a product given
        its product identifier (PID) and specific software attributes.

        :param: mdfIds: list[str]: Base mdf IDs for which to return suggested
            software releases. A maximum of 10 mdf Ids are allowed.
        """
        path = f"{SERVICE_BASE_URL}/compatible/productId/{product_id}"
        params = {
            "currentImage": current_image,
            "currentRelease": current_release,
            "supportedFeatures": supported_features,
            "supportedHardware": supported_hardware,
        }
        yield from self._session.enumerate_results(
            CompatableSoftwareResponse, path, query_params=params
        )

    @CheckSize("mdf_ids", 10)
    def get_suggestions_and_image_by_mdf_ids(
        self, mdf_ids: list[str]
    ) -> Iterable[Suggestion]:
        """
        Returns a list of Cisco suggested software releases and images for
        a list of mdf IDs.

        :param: product_ids: list[str]: Base product IDs for which to return
            suggested software releases. A maximum of 10 PIDs are allowed.
        """
        path = f"{SERVICE_BASE_URL}/software/mdfIds/" f"{','.join(mdf_ids)}"
        yield from self._session.enumerate_results(
            SuggestionsByProductResponse, path
        )

    @CheckSize("mdf_ids", 10)
    def get_suggestions_by_mdf_ids(
        self, mdf_ids: list[str]
    ) -> Iterable[Suggestion]:
        """
        Returns a list of Cisco suggested software releases and NO images for
        a list of mdf IDs.

        :param: product_ids: list[str]: Base product IDs for which to return
            suggested software releases. A maximum of 10 PIDs are allowed.
        """
        path = f"{SERVICE_BASE_URL}/releases/mdfIds/" f"{','.join(mdf_ids)}"
        yield from self._session.enumerate_results(
            SuggestionsByProductResponse, path
        )

    def get_compatible_by_mdf_id(
        self,
        mdf_id: str,
        current_image: str = None,
        current_release: str = None,
        supported_features: list[str] = None,
        supported_hardware: list[str] = None,
    ) -> Iterable[Suggestion]:
        """
        Returns compatible and suggested software releases for a product given
        its mdf identifier (mdfId) and specific software attributes.

        :param: mdfIds: list[str]: Base mdf IDs for which to return suggested
            software releases. A maximum of 10 mdf Ids are allowed.
        """
        path = f"{SERVICE_BASE_URL}/compatible/mdfId/{mdf_id}"
        params = {
            "currentImage": current_image,
            "currentRelease": current_release,
            "supportedFeatures": supported_features,
            "supportedHardware": supported_hardware,
        }
        yield from self._session.enumerate_results(
            CompatableSoftwareResponse, path, query_params=params
        )
