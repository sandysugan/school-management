from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StudentScholarshipSchema(BaseModel):
    user_id: int
    academic_year_id: int
    scholarship_name: str
    discount_value: float
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkStudentScholarshipSchema(BaseModel):
    scholarships: List[StudentScholarshipSchema]
