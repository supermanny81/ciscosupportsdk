from typing import List, Optional

from pydantic import BaseModel, Field

from .common import ApiResponse, PrintableEnum


class Severity(PrintableEnum):
    """
    Represents the severity of a defect.

    1 (high) ... 6 (low).
    """

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"


class Status(PrintableEnum):
    """
    Status of the bug; only bugs with the specified status are returned.
    """

    OPEN = "O"
    FIXED = "F"
    TERMINATED = "T"


class DateModified(PrintableEnum):
    """
    Last modified date of the bug; only bugs modified within the specified
    time are returned.
    """

    LAST_WEEK = "1"
    LAST_30_DAYS = "2"
    LAST_6_MONTHS = "3"
    LAST_YEAR = "4"
    ALL = "5"


class SortBy(PrintableEnum):
    STATUS = "status"
    MODIFIED_DATE = "modified_date"
    SEVERITY = "severity"
    CASE_COUNT = "support_case_count"
    EARLIEST_MODIFIED_DATE = "modified_date_earliest"


# Bug details response


class Bug(BaseModel):
    id: str
    base_pid: Optional[str] = None
    behavior_changed: str
    bug_id: str
    headline: str
    description: Optional[str] = None
    product_series: Optional[str] = None
    severity: str
    status: str
    duplicate_of: Optional[str] = None
    created_date: Optional[str] = None
    last_modified_date: str
    product: str
    known_affected_releases: str
    known_fixed_releases: str
    support_case_count: str


class ListOfBugs(ApiResponse):
    items: List[Bug] = Field(..., alias="bugs")
