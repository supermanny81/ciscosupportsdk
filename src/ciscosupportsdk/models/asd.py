from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import CamelCaseApi

"""
Automated Software Distribution (ASD) v4.0 models.

The ASD metadata payload is deeply nested and Cisco omits empty branches, so
every field below carries a default. These models also allow unmodelled keys
through rather than discarding them -- the metadata tree evolves with new
software types, and silently dropping fields is worse than carrying an extra
attribute.
"""


class AsdModel(BaseModel):
    class Config:
        extra = "allow"


"""
Request types
"""


class ComplianceStatus(str, Enum):
    """Accept or decline a K9 or EULA agreement."""

    ACCEPTED = "Accepted"
    DECLINED = "Declined"

    def __str__(self) -> str:
        return self.value


class BusinessFunction(str, Enum):
    """``busFunction`` values accepted when posting the K9 agreement."""

    COMM_OR_CIVIL = "COMM_OR_CIVIL"
    GOV_OR_MIL = "GOV_OR_MIL"

    def __str__(self) -> str:
        return self.value


"""
Metadata response types
"""


class AsdImage(AsdModel):
    image_guid: Optional[str] = Field(None, alias="imageGuid")
    name: Optional[str] = None
    size: Optional[str] = None
    image_description: Optional[str] = Field(None, alias="imageDescription")
    feature_set_description: Optional[str] = Field(
        None, alias="featureSetDescription"
    )
    min_dram: Optional[str] = Field(None, alias="minDram")
    min_flash: Optional[str] = Field(None, alias="minFlash")
    encryption_software_indicator: Optional[str] = Field(
        None, alias="encryptionSoftwareIndicator"
    )
    md5: Optional[str] = None
    sha512: Optional[str] = None
    is_deleted: Optional[str] = Field(None, alias="isDeleted")
    deleted_date: Optional[str] = Field(None, alias="deletedDate")
    release_date: Optional[str] = Field(None, alias="releaseDate")
    software_advisory: Optional[Any] = Field(None, alias="softwareAdvisory")
    deferral_notice: Optional[Any] = Field(None, alias="deferralNotice")
    is_related: Optional[str] = Field(None, alias="isRelated")
    additional_entitlement: Optional[Any] = Field(
        None, alias="additionalEntitlement"
    )
    psirt_indicator: Optional[str] = Field(None, alias="psirtIndicator")
    exception: Optional[Any] = None


class AsdRelease(AsdModel):
    version: Optional[str] = None
    fcs_date: Optional[str] = Field(None, alias="fcsDate")
    message: Optional[str] = None
    life_cycle: Optional[str] = Field(None, alias="lifeCycle")
    field_notice: Optional[Any] = Field(None, alias="fieldNotice")
    security_advisory: Optional[Any] = Field(None, alias="securityAdvisory")
    docs: Optional[Any] = None
    is_suggested: Optional[str] = Field(None, alias="isSuggested")
    catalog_message: Optional[str] = Field(None, alias="catalogMessage")
    images: List[AsdImage] = Field(default_factory=list)


class AsdOperatingSystem(AsdModel):
    name: Optional[str] = None
    releases: List[AsdRelease] = Field(default_factory=list)


class AsdSoftwareType(AsdModel):
    software_type_id: Optional[str] = Field(None, alias="softwareTypeId")
    software_type_name: Optional[str] = Field(None, alias="softwareTypeName")
    operating_systems: List[AsdOperatingSystem] = Field(
        default_factory=list, alias="operatingSystems"
    )


class AsdProduct(AsdModel):
    mdf_id: Optional[str] = Field(None, alias="mdfId")
    mdf_concept_name: Optional[str] = Field(None, alias="mdfConceptName")
    software_types: List[AsdSoftwareType] = Field(
        default_factory=list, alias="softwareTypes"
    )


class AsdMetadata(AsdModel):
    pid: Optional[str] = None
    products: List[AsdProduct] = Field(default_factory=list)


class AsdPagination(AsdModel):
    page_index: int = Field(1, alias="pageIndex")
    last_index: int = Field(1, alias="lastIndex")
    total_records: Optional[int] = Field(None, alias="totalRecords")
    page_records: Optional[int] = Field(None, alias="pageRecords")


class AsdMetadataResponse(AsdModel, CamelCaseApi):
    pagination_response_record: Optional[AsdPagination] = Field(
        None, alias="pagination"
    )
    self_link: Optional[str] = Field(None, alias="selfLink")
    title: Optional[str] = None
    #: Opaque handle that must be passed back to ``get_download_urls``.
    metadata_trans_id: Optional[str] = Field(None, alias="metadataTransId")
    invalid_images: List[str] = Field(
        default_factory=list, alias="invalidImages"
    )
    items: List[AsdMetadata] = Field(default_factory=list, alias="metadata")


"""
Download response types
"""


class AsdDownload(AsdModel):
    url: Optional[str] = None
    token: Optional[str] = None
    image_guid: Optional[str] = Field(None, alias="imageGuid")
    image_name: Optional[str] = Field(None, alias="imageName")
    exception: Optional[Any] = None


class AsdAcceptanceForm(AsdModel):
    """
    Present when an agreement still has to be accepted before downloading.

    When this is populated, post the corresponding K9 or EULA agreement and
    retry the download.
    """

    k9_content: Optional[Any] = Field(None, alias="k9Content")
    eula_content: Optional[Any] = Field(None, alias="eulaContent")
    web_form: Optional[Any] = Field(None, alias="webForm")
    sub_app_version: Optional[str] = Field(None, alias="subAppVersion")


class AsdDownloadResponse(AsdModel, CamelCaseApi):
    pagination_response_record: Optional[AsdPagination] = Field(
        None, alias="pagination"
    )
    self_link: Optional[str] = Field(None, alias="selfLink")
    title: Optional[str] = None
    session_id: Optional[str] = Field(None, alias="sessionId")
    acceptance_form: Optional[AsdAcceptanceForm] = Field(
        None, alias="acceptanceForm"
    )
    items: List[AsdDownload] = Field(default_factory=list, alias="downloads")


"""
Compliance (K9 / EULA) response types
"""


class AsdUserDetails(AsdModel):
    user_id: Optional[str] = Field(None, alias="userId")
    firstname: Optional[str] = None
    fullname: Optional[str] = None
    lastname: Optional[str] = None
    user_email: Optional[str] = Field(None, alias="userEmail")


class AsdAgreement(AsdModel):
    status_code: Optional[str] = Field(None, alias="statusCode")
    status_message: Optional[str] = Field(None, alias="statusMessage")
    sub_app_version: Optional[str] = Field(None, alias="subAppVersion")
    k9_content: Optional[Any] = Field(None, alias="k9Content")
    eula_content: Optional[Any] = Field(None, alias="eulaContent")
    user_details: Optional[AsdUserDetails] = Field(None, alias="userDetails")
    web_form: Optional[Any] = Field(None, alias="webForm")


class AsdAgreementAck(AsdModel):
    status_code: Optional[str] = Field(None, alias="statusCode")
    status_message: Optional[str] = Field(None, alias="statusMessage")
