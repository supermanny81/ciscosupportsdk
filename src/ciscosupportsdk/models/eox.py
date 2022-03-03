from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

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
    os: OSType
    version: str

    def __str__(self) -> str:
        return f"{self.version},{self.os}"

    class Config:
        use_enum_values = True


"""
EoX Response Types
"""


class EoxError(BaseModel):
    error_id: str = Field(None, alias="ErrorID")
    error_description: str = Field(None, alias="ErrorDescription")
    error_data_type: str = Field(None, alias="ErrorDataType")
    error_data_value: str = Field(None, alias="ErrorDataValue")


class PaginationResponseRecord(BaseModel):
    page_index: int = Field(..., alias="PageIndex")
    last_index: int = Field(..., alias="LastIndex")
    total_records: int = Field(..., alias="TotalRecords")
    page_records: int = Field(..., alias="PageRecords")


class EoxDate(BaseModel):
    value: str
    date_format: str = Field(None, alias="dateFormat")

    def to_date(self) -> datetime.date:
        d = self.value if self.value != "" else "2099-01-01"
        return datetime.strptime(d, "%Y-%m-%d").date()


class EoxMigrationDetails(BaseModel):
    pid_active_flag: str = Field(..., alias="PIDActiveFlag")
    migration_information: str = Field(..., alias="MigrationInformation")
    migration_option: str = Field(..., alias="MigrationOption")
    migration_product_id: str = Field(..., alias="MigrationProductId")
    migration_product_name: str = Field(..., alias="MigrationProductName")
    migration_strategy: str = Field(..., alias="MigrationStrategy")
    migration_product_info_url: str = Field(
        ..., alias="MigrationProductInfoURL"
    )


class EoxRecord(BaseModel):
    eol_product_id: str = Field(..., alias="EOLProductID")
    product_id_description: str = Field(..., alias="ProductIDDescription")
    product_bulletin_number: str = Field(..., alias="ProductBulletinNumber")
    link_to_product_bulletin_url: str = Field(
        ..., alias="LinkToProductBulletinURL"
    )  # noqa
    eox_external_announcement_date: EoxDate = Field(
        ..., alias="EOXExternalAnnouncementDate"
    )
    end_of_sale_date: EoxDate = Field(..., alias="EndOfSaleDate")
    end_of_sw_maintenance_releases: EoxDate = Field(
        ..., alias="EndOfSWMaintenanceReleases"
    )
    end_of_security_vul_support_date: Optional[EoxDate] = Field(
        None, alias="EndOfSecurityVulSupportDate"
    )
    end_of_routine_failure_analysis_date: EoxDate = Field(
        ..., alias="EndOfRoutineFailureAnalysisDate"
    )
    end_of_service_contract_renewal: EoxDate = Field(
        ..., alias="EndOfServiceContractRenewal"
    )
    last_date_of_support: EoxDate = Field(..., alias="LastDateOfSupport")
    end_of_svc_attach_date: EoxDate = Field(..., alias="EndOfSvcAttachDate")
    updated_time_stamp: EoxDate = Field(..., alias="UpdatedTimeStamp")
    eox_migration_details: EoxMigrationDetails = Field(
        ..., alias="EOXMigrationDetails"
    )
    eox_input_type: str = Field(..., alias="EOXInputType")
    eox_input_value: str = Field(..., alias="EOXInputValue")
    eox_error: Optional[EoxError] = Field(None, alias="EOXError")


class EoxResponse(BaseModel):
    pagination_response_record: PaginationResponseRecord = Field(
        ..., alias="PaginationResponseRecord"
    )
    eox_record: List[EoxRecord] = Field(..., alias="EOXRecord")
