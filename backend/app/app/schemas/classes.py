from pydantic import BaseModel
from typing import Optional,List

class ClassSchema(BaseModel):
    class_name: str
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class BulkClassSchema(BaseModel):
    classes: List[ClassSchema]
