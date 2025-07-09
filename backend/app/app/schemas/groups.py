from pydantic import BaseModel
from typing import Optional

class GroupSchema(BaseModel):
    group_name: str
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


