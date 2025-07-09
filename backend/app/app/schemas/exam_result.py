from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExamResultSchema(BaseModel):
    student_id: int
    exam_id: int
    allocation_id: int
    total_obtained: int
    status: Optional[str] = "pending"
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkExamResultSchema(BaseModel):
    results: List[ExamResultSchema]
