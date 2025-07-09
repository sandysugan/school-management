from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SchoolFeesSchema(BaseModel):
    academic_year_id: int
    class_id: int
    group_id: Optional[int] = None
    fee_type: str
    amount: int
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkSchoolFeesSchema(BaseModel):
    fees: List[SchoolFeesSchema]
