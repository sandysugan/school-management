from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExamSchema(BaseModel):
    allocation_id: int
    exam_name: str
    exam_code: str
    total_marks: Optional[int] = None
    start_date: datetime
    end_date: datetime
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkExamSchema(BaseModel):
    exams: List[ExamSchema]
