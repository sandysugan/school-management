from pydantic import BaseModel
from typing import Optional, List

class StudentTransportSchema(BaseModel):
    student_id: int
    bus_id: int
    pickup_point: Optional[str] = None
    drop_point: Optional[str] = None
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkStudentTransportSchema(BaseModel):
    transports: List[StudentTransportSchema]
