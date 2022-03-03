from typing import List, Optional

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
    bugs: List[str]
    case_id: str
    contact_name: str
    contract_id: str
    creation_date: str
    item_entry_id: Optional[int]
    rmas: List[str]
    serial_number: str
    status: str
    sub_technology_name: Optional[str]
    status_flag: Optional[str]
    severity: str
    technology_name: Optional[str]
    title: str
    user_id: str
    updated_date: str


class CaseSummaryResponse(ApiResponse):
    items: List[Case] = Field(..., alias="cases")
    count: int


"""
Case detail response
"""


class Note(BaseModel):
    note: str
    note_detail: str
    created_by: str
    creation_date: str


class CaseDetail(Case):
    contact_user_id: str
    preferred_contact_method: str
    contact_email_ids: List[str]
    contact_business_phone_numbers: List[str]
    contact_mobile_phone_numbers: List
    owner_name: str
    owner_email: str
    close_date: str
    tracking_number: str
    problem_code_name: str
    request_type: str
    notes: List[Note]


class CaseDetailResponse(BaseModel):
    items: CaseDetail = Field(..., alias="caseDetail")


"""
Cases response
"""


class CaseResponse(ApiResponse):
    items: List[Case] = Field(..., alias="cases")
