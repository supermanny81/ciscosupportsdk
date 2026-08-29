from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import (
    CamelCaseApi,
    PaginationResponseRecord,
)

# The Software Suggestion API omits empty and null fields from its responses
# entirely, so every field below carries a default. ``errorDetailsResponse`` in
# particular is only present when a lookup failed, which is the exception
# rather than the rule.


class Product(BaseModel):
    base_pid: Optional[str] = Field(None, alias="basePID")
    mdf_id: Optional[str] = Field(None, alias="mdfId")
    product_name: Optional[str] = Field(None, alias="productName")
    software_type: Optional[str] = Field(None, alias="softwareType")


class Image(BaseModel):
    name: Optional[str] = Field(None, alias="imageName")
    size: Optional[str] = Field(None, alias="imageSize")
    feature_set: Optional[str] = Field(None, alias="featureSet")
    description: Optional[str] = None
    required_dram: Optional[str] = Field(None, alias="requiredDRAM")
    required_flash: Optional[str] = Field(None, alias="requiredFlash")


class ErrorDetails(BaseModel):
    error_code: Optional[str] = Field(None, alias="errorCode")
    error_description: Optional[str] = Field(None, alias="errorDescription")
    suggested_action: Optional[str] = Field(None, alias="suggestedAction")
    input_identifier: Optional[str] = Field(None, alias="inputIdentifier")


class Suggestion(BaseModel):
    id: Optional[str] = None
    is_suggested: Optional[bool] = Field(None, alias="isSuggested")
    release_format1: Optional[str] = Field(None, alias="releaseFormat1")
    release_format2: Optional[str] = Field(None, alias="releaseFormat2")
    release_date: Optional[str] = Field(None, alias="releaseDate")
    major_release: Optional[str] = Field(None, alias="majorRelease")
    release_train: Optional[str] = Field(None, alias="releaseTrain")
    release_life_cycle: Optional[str] = Field(None, alias="releaseLifeCycle")
    rel_display_name: Optional[str] = Field(None, alias="relDispName")
    train_display_name: Optional[str] = Field(None, alias="trainDispName")
    images: List[Image] = Field(default_factory=list)
    error_details_response: Optional[ErrorDetails] = Field(
        None, alias="errorDetailsResponse"
    )


class Suggestions(BaseModel):
    id: Optional[str] = None
    product: Optional[Product] = None
    suggestions: List[Suggestion] = Field(default_factory=list)


class SuggestionsByProductResponse(BaseModel, CamelCaseApi):
    pagination_response_record: Optional[PaginationResponseRecord] = Field(
        None, alias="paginationResponseRecord"
    )
    items: List[Suggestions] = Field(default_factory=list, alias="productList")
    status: Optional[str] = None
    error_details_response: Optional[ErrorDetails] = Field(
        None, alias="errorDetailsResponse"
    )


class CompatableSoftwareResponse(BaseModel, CamelCaseApi):
    pagination_response_record: Optional[PaginationResponseRecord] = Field(
        None, alias="paginationResponseRecord"
    )
    items: List[Suggestion] = Field(default_factory=list, alias="suggestions")
    status: Optional[str] = None
    error_details_response: Optional[ErrorDetails] = Field(
        None, alias="errorDetailsResponse"
    )
