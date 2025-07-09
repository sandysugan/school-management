from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class AllocatedMemberSchema(BaseModel):
    allocation_id: int
    user_id: int
    subject_id: Optional[int] = None
    is_subject_teacher:Optional[int]=0
    role:str
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None
    
class BulkAllocatedMember(BaseModel):
    allocated_member:List[AllocatedMemberSchema]