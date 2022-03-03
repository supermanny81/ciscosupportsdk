from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import PaginationResponseRecord

"""
Coverage Status Response Objects
"""


class CoverageStatus(BaseModel):
    serial_number: str = Field(..., alias="sr_no")
    is_covered: bool
    coverage_end_date: str


class CoverageStatusResponse(BaseModel):
    items: List[CoverageStatus] = Field(..., alias="serial_numbers")


"""
Coverage Summary Response Objects
"""


class BasePidListItem(BaseModel):
    base_pid: str


class CSOrderablePidListItem(BaseModel):
    item_description: str
    item_position: str
    item_type: str
    orderable_pid: str
    pillar_code: str


class Coverage(BaseModel):
    id: str
    contract_site_customer_name: str
    contract_site_address1: str
    contract_site_city: str
    contract_site_state_province: str
    contract_site_country: str
    covered_product_line_end_date: str
    is_covered: bool
    sr_no: str
    warranty_end_date: str
    warranty_type: str
    warranty_type_description: str
    service_contract_number: str
    service_line_descr: str


class CoverageSummary(Coverage):
    base_pid_list: List[BasePidListItem]
    orderable_pid_list: List[CSOrderablePidListItem]
    parent_sr_no: str


class CoverageSummaryResponse(BaseModel):
    pagination_response_record: PaginationResponseRecord
    items: List[CoverageSummary] = Field(..., alias="serial_numbers")


"""
Coverage Summary Response Objects - when using an instance ID
"""


class CSIBasePid(BaseModel):
    base_pid: str


class CSIOrderablePid(BaseModel):
    item_description: str
    item_position: str
    item_type: str
    orderable_pid: str


class CoverageSummaryByInstance(Coverage):
    base_pid: CSIBasePid
    instance_number: str
    parent_instance_no: str
    orderable_pid: CSIOrderablePid


class CoverageSummaryByInstanceResponse(BaseModel):
    pagination_response_record: PaginationResponseRecord
    items: List[CoverageSummaryByInstance] = Field(
        ..., alias="instance_numbers"
    )


"""
Orderable Product IDs by Serial Number Response Objects
"""


class OrderablePidListItem(BaseModel):
    orderable_pid: str
    pillar_code: str
    pillar_description: str


class OrderableProductList(BaseModel):
    sr_no: str
    orderable_pid_list: List[OrderablePidListItem]


class OrderableProductListResponse(BaseModel):
    items: List[OrderableProductList] = Field(..., alias="serial_numbers")


"""
Coverage Owner Status Response
"""


class CoverageOwnerStatus(CoverageStatus):
    is_owner: bool = Field(..., alias="sr_no_owner")


class CoverageOwnerStatusResponse(BaseModel):
    items: List[CoverageOwnerStatus] = Field(..., alias="serial_numbers")
