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
 
class StudentAttendanceFilterSchema(BaseModel):
    student_id: Optional[int] = None
    allocation_id: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None