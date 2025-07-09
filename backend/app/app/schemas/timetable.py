from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TimeTableSchema(BaseModel):
    allocation_id: int
    subject_id: int
    teacher_id: int
    period_id: int
    day_id: int
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkTimeTableSchema(BaseModel):
    timetables: List[TimeTableSchema]
