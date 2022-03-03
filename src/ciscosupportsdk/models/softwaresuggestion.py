from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ciscosupportsdk.models.common import (
    CamelCaseApi,
    PaginationResponseRecord,
)


class Product(BaseModel):
    base_pid: Optional[str] = Field(None, alias="basePID")
    mdf_id: str = Field(..., alias="mdfId")
    product_name: str = Field(..., alias="productName")
    software_type: str = Field(..., alias="softwareType")


class Image(BaseModel):
    name: str = Field(..., alias="imageName")
    size: str = Field(..., alias="imageSize")
    feature_set: Optional[str] = Field(None, alias="featureSet")
    description: Optional[str]
    required_dram: str = Field(..., alias="requiredDRAM")
    required_flash: str = Field(..., alias="requiredFlash")


class ErrorDetails(BaseModel):
    error_code: str = Field(..., alias="errorCode")
    error_description: str = Field(..., alias="errorDescription")
    suggested_action: str = Field(..., alias="suggestedAction")
    input_identifier: str = Field(..., alias="inputIdentifier")


class Suggestion(BaseModel):
    id: str
    is_suggested: bool = Field(..., alias="isSuggested")
    release_format1: str = Field(..., alias="releaseFormat1")
    release_format2: str = Field(..., alias="releaseFormat2")
    release_date: str = Field(..., alias="releaseDate")
    major_release: str = Field(..., alias="majorRelease")
    release_train: str = Field(..., alias="releaseTrain")
    release_life_cycle: str = Field(..., alias="releaseLifeCycle")
    rel_display_name: str = Field(..., alias="relDispName")
    train_display_name: str = Field(..., alias="trainDispName")
    images: Optional[List[Image]]
    error_details_response: Optional[ErrorDetails] = Field(
        ..., alias="errorDetailsResponse"
    )


class Suggestions(BaseModel):
    id: str
    product: Product
    suggestions: List[Suggestion]


class SuggestionsByProductResponse(BaseModel, CamelCaseApi):
    pagination_response_record: PaginationResponseRecord = Field(
        ..., alias="paginationResponseRecord"
    )
    items: List[Suggestions] = Field(..., alias="productList")
    status: str
    error_details_response: Optional[ErrorDetails] = Field(
        ..., alias="errorDetailsResponse"
    )


class CompatableSoftwareResponse(BaseModel, CamelCaseApi):
    pagination_response_record: PaginationResponseRecord = Field(
        ..., alias="paginationResponseRecord"
    )
    items: List[Suggestion] = Field(..., alias="suggestions")
    status: str
    error_details_response: Optional[ErrorDetails] = Field(
        ..., alias="errorDetailsResponse"
    )
