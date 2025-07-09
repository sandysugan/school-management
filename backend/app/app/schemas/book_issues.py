from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BookIssueSchema(BaseModel):
    book_id: int
    student_id: int
    issue_date: Optional[datetime] = None
    due_date: datetime
    return_date: Optional[datetime] = None
    status: Optional[str] = "issued"
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkBookIssueSchema(BaseModel):
    issues: List[BookIssueSchema]
