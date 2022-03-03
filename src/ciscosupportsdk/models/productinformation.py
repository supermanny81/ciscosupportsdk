from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import ApiResponse


class Dimensions(BaseModel):
    dimensions_format: str
    dimensions_value: str


class RichMediaUrls(BaseModel):
    large_image_url: str
    small_image_url: str


class ProductInformationRecord(BaseModel):
    id: str
    product_id: Optional[str]
    product_name: str
    product_type: str
    product_series: str
    product_category: str
    product_subcategory: str
    release_date: str
    orderable_status: str
    dimensions: Dimensions
    weight: str
    form_factor: str
    product_support_page: str
    visio_stencil_url: str
    rich_media_urls: RichMediaUrls


class ProductInformationResponse(ApiResponse):
    items: List[ProductInformationRecord] = Field(..., alias="product_list")


class ProductMDFRecord(BaseModel):
    id: str
    product_id: str
    product_name: str
    product_name_mdf: str
    product_series: str
    product_series_mdf: str


class ProductMDFResponse(ApiResponse):
    items: List[ProductMDFRecord] = Field(..., alias="product_list")
