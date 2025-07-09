from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StudentFeesSchema(BaseModel):
    student_id: int
    scl_fee_id: int
    scholarship_id: Optional[int] = None
    paid_amount: int = 0
    due_date: Optional[datetime] = None
    payment_mode: Optional[str] = None
    payment_date: Optional[datetime] = None
    receipt_no: Optional[str] = None
    status: Optional[str] = "pending"
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkStudentFeesSchema(BaseModel):
    fees: List[StudentFeesSchema]
