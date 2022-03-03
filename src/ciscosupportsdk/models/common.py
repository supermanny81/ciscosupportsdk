from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PrintableEnum(Enum):
    def __str__(self):
        return self.value


class PaginationResponseRecord(BaseModel):
    title: str
    page_index: int = Field(..., alias="pageIndex")
    last_index: int = Field(..., alias="lastIndex")
    total_records: int = Field(..., alias="totalRecords")
    page_records: int = Field(..., alias="pageRecords")
    self_link: str = Field(..., alias="selfLink")

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
