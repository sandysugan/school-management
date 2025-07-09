from pydantic import BaseModel
from typing import Optional,List

class AllocationSchema(BaseModel):
    academic_year_id: int
    class_id: int
    section_id: int
    group_id: Optional[int] = None
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkAllocationSchema(BaseModel):
    allocations: List[AllocationSchema]