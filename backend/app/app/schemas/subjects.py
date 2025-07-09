from pydantic import BaseModel
from typing import Optional, List

class SubjectSchema(BaseModel):
    subject_name: str
    subject_code: str
    group_id: Optional[int] = None
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkSubjectSchema(BaseModel):
    subjects: List[SubjectSchema]
