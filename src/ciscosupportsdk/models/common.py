from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PrintableEnum(Enum):
    def __str__(self):
        return self.value


class PaginationResponseRecord(BaseModel):
    # Pagination blocks are occasionally returned partially populated. The
    # index fields default to 1 so that a missing block reads as "a single
    # page of results" rather than failing validation.
    title: Optional[str] = None
    page_index: int = Field(1, alias="pageIndex")
    last_index: int = Field(1, alias="lastIndex")
    total_records: Optional[int] = Field(None, alias="totalRecords")
    page_records: Optional[int] = Field(None, alias="pageRecords")
    self_link: Optional[str] = Field(None, alias="selfLink")

    class Config:
        allow_population_by_field_name = True


class CamelCaseApi(object):
    """
    Used to annotate request behavior
    """

    pass


class ApiResponse(BaseModel):
    pagination_response_record: Optional[PaginationResponseRecord] = None
    items: List[BaseModel]
