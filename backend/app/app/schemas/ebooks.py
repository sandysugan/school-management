from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EBookSchema(BaseModel):
    subject_id: int
    title: str
    file_url: str
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkEBookSchema(BaseModel):
    ebooks: List[EBookSchema]
