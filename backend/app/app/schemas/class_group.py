from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClassGroupSchema(BaseModel):
    class_id: int
    group_id: int
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkClassGroupSchema(BaseModel):
    class_groups: list[ClassGroupSchema]
