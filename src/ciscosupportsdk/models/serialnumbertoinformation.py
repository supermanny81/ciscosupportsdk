from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import PaginationResponseRecord

# Coverage payloads are sparse by design: contract, warranty and site fields
# are simply absent for serial numbers that are not covered, so everything
# apart from the identifier itself carries a default.

"""
Coverage Status Response Objects
"""


class CoverageStatus(BaseModel):
    serial_number: Optional[str] = Field(None, alias="sr_no")
    is_covered: Optional[bool] = None
    coverage_end_date: Optional[str] = None


class CoverageStatusResponse(BaseModel):
    items: List[CoverageStatus] = Field(
        default_factory=list, alias="serial_numbers"
    )


"""
Coverage Summary Response Objects
"""


class BasePidListItem(BaseModel):
    base_pid: Optional[str] = None


class CSOrderablePidListItem(BaseModel):
    item_description: Optional[str] = None
    item_position: Optional[str] = None
    item_type: Optional[str] = None
    orderable_pid: Optional[str] = None
    pillar_code: Optional[str] = None


class Coverage(BaseModel):
    id: Optional[str] = None
    contract_site_customer_name: Optional[str] = None
    contract_site_address1: Optional[str] = None
    contract_site_city: Optional[str] = None
    contract_site_state_province: Optional[str] = None
    contract_site_country: Optional[str] = None
    contract_site_postal_code: Optional[str] = None
    covered_product_line_end_date: Optional[str] = None
    is_covered: Optional[bool] = None
    sr_no: Optional[str] = None
    warranty_end_date: Optional[str] = None
    warranty_type: Optional[str] = None
    warranty_type_description: Optional[str] = None
    service_contract_number: Optional[str] = None
    service_line_descr: Optional[str] = None


class CoverageSummary(Coverage):
    base_pid_list: List[BasePidListItem] = Field(default_factory=list)
    orderable_pid_list: List[CSOrderablePidListItem] = Field(
        default_factory=list
    )
    parent_sr_no: Optional[str] = None


class CoverageSummaryResponse(BaseModel):
    pagination_response_record: Optional[PaginationResponseRecord] = None
    items: List[CoverageSummary] = Field(
        default_factory=list, alias="serial_numbers"
    )


"""
Coverage Summary Response Objects - when using an instance ID
"""


class CSIBasePid(BaseModel):
    base_pid: Optional[str] = None


class CSIOrderablePid(BaseModel):
    item_description: Optional[str] = None
    item_position: Optional[str] = None
    item_type: Optional[str] = None
    orderable_pid: Optional[str] = None


class CoverageSummaryByInstance(Coverage):
    base_pid: Optional[CSIBasePid] = None
    instance_number: Optional[str] = None
    parent_instance_no: Optional[str] = None
    orderable_pid: Optional[CSIOrderablePid] = None


class CoverageSummaryByInstanceResponse(BaseModel):
    pagination_response_record: Optional[PaginationResponseRecord] = None
    items: List[CoverageSummaryByInstance] = Field(
        default_factory=list, alias="instance_numbers"
    )


"""
Orderable Product IDs by Serial Number Response Objects
"""


class OrderablePidListItem(BaseModel):
    orderable_pid: Optional[str] = None
    pillar_code: Optional[str] = None
    pillar_description: Optional[str] = None


class OrderableProductList(BaseModel):
    sr_no: Optional[str] = None
    orderable_pid_list: List[OrderablePidListItem] = Field(
        default_factory=list
    )


class OrderableProductListResponse(BaseModel):
    items: List[OrderableProductList] = Field(
        default_factory=list, alias="serial_numbers"
    )


"""
Coverage Owner Status Response
"""


class CoverageOwnerStatus(CoverageStatus):
    is_owner: Optional[bool] = Field(None, alias="sr_no_owner")


class CoverageOwnerStatusResponse(BaseModel):
    items: List[CoverageOwnerStatus] = Field(
        default_factory=list, alias="serial_numbers"
    )
