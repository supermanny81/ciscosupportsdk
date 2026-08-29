from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import ApiResponse

# Release 1.0 of the Product Information API only covers hardware, and it omits
# fields it has no value for (physical dimensions, imagery, and so on), so all
# fields carry defaults.


class Dimensions(BaseModel):
    dimensions_format: Optional[str] = None
    dimensions_value: Optional[str] = None


class RichMediaUrls(BaseModel):
    large_image_url: Optional[str] = None
    small_image_url: Optional[str] = None


class ProductInformationRecord(BaseModel):
    id: Optional[str] = None
    # ``sr_no`` is echoed back on the by-serial-number endpoint and is the only
    # way to correlate a record with the serial number that was queried.
    sr_no: Optional[str] = None
    base_pid: Optional[str] = None
    orderable_pid: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    product_type: Optional[str] = None
    product_series: Optional[str] = None
    product_category: Optional[str] = None
    product_subcategory: Optional[str] = None
    release_date: Optional[str] = None
    orderable_status: Optional[str] = None
    dimensions: Optional[Dimensions] = None
    weight: Optional[str] = None
    form_factor: Optional[str] = None
    product_support_page: Optional[str] = None
    visio_stencil_url: Optional[str] = None
    rich_media_urls: Optional[RichMediaUrls] = None


class ProductInformationResponse(ApiResponse):
    items: List[ProductInformationRecord] = Field(
        default_factory=list, alias="product_list"
    )


class ProductMDFRecord(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    product_name_mdf: Optional[str] = None
    product_series: Optional[str] = None
    product_series_mdf: Optional[str] = None


class ProductMDFResponse(ApiResponse):
    items: List[ProductMDFRecord] = Field(
        default_factory=list, alias="product_list"
    )
