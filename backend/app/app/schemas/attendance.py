from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AttendanceSchema(BaseModel):
    user_id: int
    allocation_id: int
    date: date
    status: str  # Present, Absent, Half day
    created_by: Optional[int] = None 
    updated_by: Optional[int] = None

class BulkAttendanceSchema(BaseModel):
    records: List[AttendanceSchema]

class AttendanceReportFilter(BaseModel):
    from_date: Optional[date]
    to_date: Optional[date]
    user_id: Optional[int]
    allocation_id: Optional[int]

class AttendanceReportRecord(BaseModel):
    date: str
    status: str
    user_id: int
    name: str

class AttendanceReportResponse(BaseModel):
    status: int
    total_days: int
    present: float
    absent: int
    half_day: int
    percentage: float
    records: List[AttendanceReportRecord]