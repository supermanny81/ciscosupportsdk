from ciscosupportsdk.apisession import ApiSession

from .asd import AutomatedSoftwareDistributionApi
from .bug import BugApi
from .case import CaseApi
from .eox import EoxApi
from .productinformation import ProductInformationApi
from .serialnumbertoinformation import SerialNumberToInformationAPI
from .serviceorderreturn import ServiceOrderReturnApi
from .softwaresuggestion import SoftwareSuggestionApi


class CiscoSupportAPI(object):
    """Cisco Support API wrapper.

    Creates a session for all API calls through a CiscoSupportAPI
    object.  The 'session' handles authentication and communication
    to the API.  Each of the support APIs are added to this object
    in a hierarchical structure.
    """

    def __init__(self, client_id: str, client_secret: str):
        self._session = ApiSession(client_id, client_secret)

        # setup the rest of the APIs
        self.asd = AutomatedSoftwareDistributionApi(self._session)
        self.bug = BugApi(self._session)
        self.case = CaseApi(self._session)
        self.eox = EoxApi(self._session)
        self.product_information = ProductInformationApi(self._session)
        self.serial_information = SerialNumberToInformationAPI(self._session)
        self.suggestion = SoftwareSuggestionApi(self._session)
        self.rma = ServiceOrderReturnApi(self._session)
        # just in case
        self.service_order_return = self.rma
