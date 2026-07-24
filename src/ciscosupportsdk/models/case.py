from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .common import ApiResponse, PrintableEnum

"""
Case request items
"""


class SortCaseBy(PrintableEnum):
    UPDATED_DATE = "UPDATED_DATE"
    STATUS = "STATUS"


class CaseStatusFlag(PrintableEnum):
    OPEN = "O"
    CLOSED = "C"


"""
Case Response Items
"""


class Case(BaseModel):
    # The Cisco Support Case API returns sparse objects: fields that do not
    # apply to a given case (e.g. state-dependent or optional data) are omitted
    # from the payload entirely. Only ``case_id`` is guaranteed to be present,
    # so every other field carries a default to keep validation resilient. List
    # fields default to an empty list so consumers can always iterate them.
    case_id: str
    bugs: List[str] = Field(default_factory=list)
    contact_name: Optional[str] = None
    contract_id: Optional[str] = None
    creation_date: Optional[str] = None
    item_entry_id: Optional[int] = None
    rmas: List[str] = Field(default_factory=list)
    serial_number: Optional[str] = None
    status: Optional[str] = None
    sub_technology_name: Optional[str] = None
    status_flag: Optional[str] = None
    severity: Optional[str] = None
    technology_name: Optional[str] = None
    title: Optional[str] = None
    user_id: Optional[str] = None
    updated_date: Optional[str] = None


class CaseSummaryResponse(ApiResponse):
    items: List[Case] = Field(..., alias="cases")
    count: int


"""
Case detail response
"""


class Note(BaseModel):
    note: Optional[str] = None
    note_detail: Optional[str] = None
    created_by: Optional[str] = None
    creation_date: Optional[str] = None


class CaseDetail(Case):
    # As with ``Case``, detail fields are frequently absent depending on case
    # state (e.g. ``close_date`` is only present for closed cases). All fields
    # therefore carry defaults so validation never fails on a sparse payload.
    contact_user_id: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    contact_email_ids: List[str] = Field(default_factory=list)
    contact_business_phone_numbers: List[str] = Field(default_factory=list)
    contact_mobile_phone_numbers: List = Field(default_factory=list)
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    close_date: Optional[str] = None
    tracking_number: Optional[str] = None
    problem_code_name: Optional[str] = None
    request_type: Optional[str] = None
    notes: List[Note] = Field(default_factory=list)
    # Stretch fields surfaced by the v3 detail endpoint when available. Their
    # exact shape is not covered by the recorded fixtures, so they are typed
    # permissively; refine once a confirmed payload is available.
    rma_numbers: List[str] = Field(default_factory=list)
    crashinfo: Optional[Any] = None


class CaseDetailResponse(BaseModel):
    items: CaseDetail = Field(..., alias="caseDetail")


"""
Cases response
"""


class CaseResponse(ApiResponse):
    items: List[Case] = Field(..., alias="cases")
