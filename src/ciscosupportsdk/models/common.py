from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class PrintableEnum(Enum):
    def __str__(self):
        return self.value


class PaginationResponseRecord(BaseModel):
    # Accept both the wire aliases (pageIndex) and the field names
    # (page_index), so callers can construct these directly.
    model_config = ConfigDict(populate_by_name=True)

    # Pagination blocks are occasionally returned partially populated. The
    # index fields default to 1 so that a missing block reads as "a single
    # page of results" rather than failing validation.
    title: Optional[str] = None
    page_index: int = Field(1, alias="pageIndex")
    last_index: int = Field(1, alias="lastIndex")
    total_records: Optional[int] = Field(None, alias="totalRecords")
    page_records: Optional[int] = Field(None, alias="pageRecords")
    self_link: Optional[str] = Field(None, alias="selfLink")


class CamelCaseApi(object):
    """
    Used to annotate request behavior
    """

    pass


class ApiResponse(BaseModel):
    # ``items`` is always overridden by a subclass with the concrete record
    # type. It is annotated as Any rather than List[BaseModel] because
    # pydantic v2 validates a bare BaseModel annotation by discarding every
    # field of whatever is passed in.
    pagination_response_record: Optional[PaginationResponseRecord] = None
    items: Any = None
