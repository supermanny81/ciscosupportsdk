from typing import Iterable, Optional

from ciscosupportsdk.apisession import ApiSession
from ciscosupportsdk.models.asd import (
    AsdAgreement,
    AsdAgreementAck,
    AsdDownload,
    AsdDownloadResponse,
    AsdMetadata,
    AsdMetadataResponse,
    BusinessFunction,
    ComplianceStatus,
)

SERVICE_BASE_URL = "/software/v4.0"


class AutomatedSoftwareDistributionApi(object):
    """
    Cisco Automated Software Distribution service provides software
    information and download URLs to assist you in upgrading your
    device/application to the latest version.

    Unlike the other Support APIs, ASD takes its inputs as a JSON request
    body over POST rather than as path parameters.

    A download is a two step flow: call one of the metadata methods to get
    image GUIDs and a ``metadata_trans_id``, then pass both to
    :meth:`get_download_urls`. If the response carries an ``acceptance_form``,
    the K9 or EULA agreement still has to be accepted -- post it with
    :meth:`accept_k9_agreement` or :meth:`accept_eula_agreement` and retry.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    def _paged_metadata(
        self, path: str, body: dict, per_page: Optional[int]
    ) -> Iterable[AsdMetadata]:
        """Walks the metadata pages for a POST endpoint."""
        page_index = 1
        while True:
            payload = dict(body)
            payload["pageIndex"] = page_index
            if per_page is not None:
                payload["perPage"] = per_page

            json = self._session._post(path, json=payload)
            response = AsdMetadataResponse(**json)
            yield from response.items

            pages = response.pagination_response_record
            if pages is None or pages.page_index >= pages.last_index:
                return
            page_index = pages.page_index + 1

    def get_software_by_pid_and_release(
        self,
        pid: str,
        current_release_version: str,
        output_release_version: str = "latest",
        per_page: int = None,
    ) -> Iterable[AsdMetadata]:
        """
        Returns software metadata for a product ID and release version.

        :param: pid: str: Product identifier to return software for.
        :param: current_release_version: str: Release currently running on
            the device, for example ``5.4.3``.
        :param: output_release_version: str: Release to return metadata for;
            ``latest`` returns the most recent release.
        :param: per_page: int: Number of records to return per page.
        :rtype: Iterable[AsdMetadata]
        """
        path = f"{SERVICE_BASE_URL}/metadata/pidrelease"
        body = {
            "pid": pid,
            "currentReleaseVersion": current_release_version,
            "outputReleaseVersion": output_release_version,
        }
        yield from self._paged_metadata(path, body, per_page)

    def get_software_by_pid_and_image(
        self,
        pid: str,
        image_names: list[str],
        per_page: int = None,
    ) -> Iterable[AsdMetadata]:
        """
        Returns software metadata for a product ID and image name or names.

        :param: pid: str: Product identifier to return software for.
        :param: image_names: list[str]: Image names to return metadata for.
        :param: per_page: int: Number of records to return per page.
        :rtype: Iterable[AsdMetadata]
        """
        path = f"{SERVICE_BASE_URL}/metadata/pidimage"
        body = {"pid": pid, "imageNames": image_names}
        yield from self._paged_metadata(path, body, per_page)

    def get_software_status_by_image(
        self, image_names: list[str]
    ) -> AsdMetadataResponse:
        """
        Returns the current status of the specified image or images.

        Unlike the other metadata endpoints this one is not paginated, and
        the full response is returned so that ``invalid_images`` -- the names
        the service did not recognise -- is available to the caller.

        :param: image_names: list[str]: Image names to look up.
        :rtype: AsdMetadataResponse
        """
        path = f"{SERVICE_BASE_URL}/metadata/images"
        json = self._session._post(path, json={"imageNames": image_names})
        return AsdMetadataResponse(**json)

    def get_download_urls(
        self,
        pid: str,
        mdf_id: str,
        metadata_trans_id: str,
        image_guids: list[str],
    ) -> AsdDownloadResponse:
        """
        Returns sessionized download URLs for the specified images.

        The whole response is returned rather than just the downloads,
        because ``acceptance_form`` has to be inspected: when it is populated
        the K9 or EULA agreement must be accepted before the URLs are usable.

        :param: pid: str: Product identifier the images belong to.
        :param: mdf_id: str: MDF identifier from the metadata response.
        :param: metadata_trans_id: str: ``metadata_trans_id`` returned by the
            metadata call that produced these image GUIDs.
        :param: image_guids: list[str]: Image GUIDs to download.
        :rtype: AsdDownloadResponse
        """
        path = f"{SERVICE_BASE_URL}/download/pidimage"
        body = {
            "pid": pid,
            "mdfId": mdf_id,
            "metadataTransId": metadata_trans_id,
            "imageGuids": image_guids,
        }
        json = self._session._post(path, json=body)
        return AsdDownloadResponse(**json)

    def get_downloads(
        self,
        pid: str,
        mdf_id: str,
        metadata_trans_id: str,
        image_guids: list[str],
    ) -> Iterable[AsdDownload]:
        """
        Convenience wrapper over :meth:`get_download_urls` that yields just
        the download entries.

        :rtype: Iterable[AsdDownload]
        """
        yield from self.get_download_urls(
            pid, mdf_id, metadata_trans_id, image_guids
        ).items

    def get_k9_agreement(self) -> AsdAgreement:
        """
        Returns the K9 (strong encryption) agreement text and the current
        acceptance state for the authenticated user.

        :rtype: AsdAgreement
        """
        path = f"{SERVICE_BASE_URL}/compliance/k9"
        return AsdAgreement(**self._session._get(path, {}))

    def accept_k9_agreement(
        self,
        file_names: list[str] = None,
        status: ComplianceStatus = ComplianceStatus.ACCEPTED,
        confirm: str = "CONFIRM_CHECKED",
        bus_function: BusinessFunction = BusinessFunction.COMM_OR_CIVIL,
        gov_mil_countries: str = "GOV_OR_MIL_COUNTRIES_NO",
        decline_comments: str = None,
    ) -> AsdAgreementAck:
        """
        Records the user's response to the K9 agreement.

        :param: file_names: list[str]: Images the response applies to.
        :param: status: ComplianceStatus: Accepted or Declined.
        :param: confirm: str: Confirmation checkbox value.
        :param: bus_function: BusinessFunction: Business function declaration.
        :param: gov_mil_countries: str: Government/military country
            declaration.
        :param: decline_comments: str: Required when declining.
        :rtype: AsdAgreementAck
        """
        if status == ComplianceStatus.DECLINED and not decline_comments:
            raise ValueError(
                "decline_comments is required when status is Declined."
            )

        path = f"{SERVICE_BASE_URL}/compliance/k9"
        body = {
            "status": str(status),
            "confirm": confirm,
            "busFunction": str(bus_function),
            "govMilCountries": gov_mil_countries,
        }
        if file_names is not None:
            body["fileNames"] = ",".join(file_names)
        if decline_comments is not None:
            body["declineComments"] = decline_comments

        return AsdAgreementAck(**self._session._post(path, json=body))

    def get_eula_agreement(self) -> AsdAgreement:
        """
        Returns the EULA text and the current acceptance state for the
        authenticated user.

        :rtype: AsdAgreement
        """
        path = f"{SERVICE_BASE_URL}/compliance/eula"
        return AsdAgreement(**self._session._get(path, {}))

    def accept_eula_agreement(
        self,
        file_names: list[str] = None,
        status: ComplianceStatus = ComplianceStatus.ACCEPTED,
        decline_comments: str = None,
    ) -> AsdAgreementAck:
        """
        Records the user's response to the EULA.

        :param: file_names: list[str]: Images the response applies to.
        :param: status: ComplianceStatus: Accepted or Declined.
        :param: decline_comments: str: Required when declining.
        :rtype: AsdAgreementAck
        """
        if status == ComplianceStatus.DECLINED and not decline_comments:
            raise ValueError(
                "decline_comments is required when status is Declined."
            )

        path = f"{SERVICE_BASE_URL}/compliance/eula"
        body = {"status": str(status)}
        if file_names is not None:
            body["fileNames"] = ",".join(file_names)
        if decline_comments is not None:
            body["declineComments"] = decline_comments

        return AsdAgreementAck(**self._session._post(path, json=body))
