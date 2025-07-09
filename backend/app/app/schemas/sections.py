from pydantic import BaseModel
from typing import Optional, List

class SectionSchema(BaseModel):
    section_name: str
    class_id: int
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkSectionSchema(BaseModel):
    sections: List[SectionSchema]
