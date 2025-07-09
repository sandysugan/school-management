from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MarksSchema(BaseModel):
    student_id: int
    exam_id: int
    subject_id: int
    obtained_marks: int
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkMarksSchema(BaseModel):
    marks: List[MarksSchema]
