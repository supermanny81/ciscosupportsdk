from ciscosupportsdk.apisession import ApiSession

SERVICE_BASE_URL = "/software/v4.0"


class AutomatedSoftwareDistributionApi(object):
    """
    Cisco Automated Software Distribution service provides software
    information and download URLs to assist you in upgrading your
    device/application to the latest version.
    """

    def __init__(self, session: ApiSession) -> None:
        self._session = session

    def get_bug_details(self, bug_ids: list[str]) -> None:
        """
        Returns detailed information for the specified bug ID or IDs.

        :param: bug_ids: list[str]: Identifier of the bug or bugs for which
            to return detailed information. A maximum of five (5) bug IDs can
            be submitted separated by a comma.
        :rtype: Bug
        """
        path = f"{SERVICE_BASE_URL}/bug_ids/" f"{','.join(bug_ids)}"
        print(path)
        pass
