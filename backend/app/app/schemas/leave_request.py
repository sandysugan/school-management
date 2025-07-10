from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class LeaveRequestSchema(BaseModel):
    user_id: int
    allocation_id: int
    reason: Optional[str] = None
    from_date: date
    to_date: date
    status: Optional[str] = "Pending"
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

