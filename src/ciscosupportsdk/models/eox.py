from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

"""
EoX Request Types
"""


class EoxAttrib(str, Enum):
    EO_EXT_ANNOUNCE_DATE = "EO_EXT_ANNOUNCE_DATE"
    EO_SALES_DATE = "EO_SALES_DATE"
    EO_FAIL_ANALYSIS_DATE = "EO_FAIL_ANALYSIS_DATE"
    EO_SVC_ATTACH_DATE = "EO_SVC_ATTACH_DATE"
    EO_SW_MAINTENANCE_DATE = "EO_SW_MAINTENANCE_DATE"
    EO_SECURITY_VUL_SUPPORT_DATE = "EO_SECURITY_VUL_SUPPORT_DATE"
    EO_CONTRACT_RENEW_DATE = "EO_CONTRACT_RENEW_DATE"
    EO_LAST_SUPPORT_DATE = "EO_LAST_SUPPORT_DATE"
    UPDATE_TIMESTAMP = "UPDATE_TIMESTAMP"


class OSType(str, Enum):
    ACNS = "ACNS"
    ACSW = "ACSW"
    ALTIGAOS = "ALTIGAOS"
    ASA = "ASA"
    ASYNCOS = "ASYNCOS"
    CATOS = "CATOS"
    CDS_IS = "CDS-IS"
    CDS_TV = "CDS-TV"
    CDS_VN = "CDS-VN"
    CDS_VQE = "CDS-VQE"
    CTS = "CTS"
    ECDS = "ECDS"
    FWSM_OS = "FWSM-OS"
    GSS = "GSS"
    IOS = "IOS"
    IOS_XR = "IOS XR"
    IOS_XE = "IOS-XE"
    IPS = "IPS"
    NAM = "NAM"
    NX_OS = "NX-OS"
    ONS = "ONS"
    PIXOS = "PIXOS"
    SAN_OS = "SAN-OS"
    STAR_OS = "STAR OS"
    TC = "TC"
    TE = "TE"
    UCS_NX_OS = "UCS NX-OS"
    VCS = "VCS"
    VDS_IS = "VDS-IS"
    WAAS = "WAAS"
    WANSW_BPX_IGX_IPX = "WANSW BPX/IGX/IPX"
    WEBNS = "WEBNS"
    WLC = "WLC"
    WLSE_OS = "WLSE-OS"
    XC = "XC"


class SoftwareRelease(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    os: OSType
    version: str

    def __str__(self) -> str:
        return f"{self.version},{self.os}"


"""
EoX Response Types
"""


class EoxError(BaseModel):
    error_id: Optional[str] = Field(None, alias="ErrorID")
    error_description: Optional[str] = Field(None, alias="ErrorDescription")
    error_data_type: Optional[str] = Field(None, alias="ErrorDataType")
    error_data_value: Optional[str] = Field(None, alias="ErrorDataValue")


class PaginationResponseRecord(BaseModel):
    page_index: int = Field(1, alias="PageIndex")
    last_index: int = Field(1, alias="LastIndex")
    total_records: Optional[int] = Field(None, alias="TotalRecords")
    page_records: Optional[int] = Field(None, alias="PageRecords")


class EoxDate(BaseModel):
    value: Optional[str] = None
    date_format: Optional[str] = Field(None, alias="dateFormat")

    def to_date(self) -> datetime.date:
        d = self.value if self.value else "2099-01-01"
        return datetime.strptime(d, "%Y-%m-%d").date()


class EoxMigrationDetails(BaseModel):
    pid_active_flag: Optional[str] = Field(None, alias="PIDActiveFlag")
    migration_information: Optional[str] = Field(
        None, alias="MigrationInformation"
    )
    migration_option: Optional[str] = Field(None, alias="MigrationOption")
    migration_product_id: Optional[str] = Field(
        None, alias="MigrationProductId"
    )
    migration_product_name: Optional[str] = Field(
        None, alias="MigrationProductName"
    )
    migration_strategy: Optional[str] = Field(None, alias="MigrationStrategy")
    migration_product_info_url: Optional[str] = Field(
        None, alias="MigrationProductInfoURL"
    )


class EoxRecord(BaseModel):
    # Records for products with no migration path, or that were queried by an
    # attribute that does not apply, omit whole blocks from the payload, so
    # every field defaults.
    eol_product_id: Optional[str] = Field(None, alias="EOLProductID")
    product_id_description: Optional[str] = Field(
        None, alias="ProductIDDescription"
    )
    product_bulletin_number: Optional[str] = Field(
        None, alias="ProductBulletinNumber"
    )
    link_to_product_bulletin_url: Optional[str] = Field(
        None, alias="LinkToProductBulletinURL"
    )  # noqa
    eox_external_announcement_date: Optional[EoxDate] = Field(
        None, alias="EOXExternalAnnouncementDate"
    )
    end_of_sale_date: Optional[EoxDate] = Field(None, alias="EndOfSaleDate")
    end_of_sw_maintenance_releases: Optional[EoxDate] = Field(
        None, alias="EndOfSWMaintenanceReleases"
    )
    end_of_security_vul_support_date: Optional[EoxDate] = Field(
        None, alias="EndOfSecurityVulSupportDate"
    )
    end_of_routine_failure_analysis_date: Optional[EoxDate] = Field(
        None, alias="EndOfRoutineFailureAnalysisDate"
    )
    end_of_service_contract_renewal: Optional[EoxDate] = Field(
        None, alias="EndOfServiceContractRenewal"
    )
    last_date_of_support: Optional[EoxDate] = Field(
        None, alias="LastDateOfSupport"
    )
    end_of_svc_attach_date: Optional[EoxDate] = Field(
        None, alias="EndOfSvcAttachDate"
    )
    updated_time_stamp: Optional[EoxDate] = Field(
        None, alias="UpdatedTimeStamp"
    )
    eox_migration_details: Optional[EoxMigrationDetails] = Field(
        None, alias="EOXMigrationDetails"
    )
    eox_input_type: Optional[str] = Field(None, alias="EOXInputType")
    eox_input_value: Optional[str] = Field(None, alias="EOXInputValue")
    eox_error: Optional[EoxError] = Field(None, alias="EOXError")


class EoxResponse(BaseModel):
    pagination_response_record: PaginationResponseRecord = Field(
        default_factory=PaginationResponseRecord,
        alias="PaginationResponseRecord",
    )
    eox_record: List[EoxRecord] = Field(
        default_factory=list, alias="EOXRecord"
    )
