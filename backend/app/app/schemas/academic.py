from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class AcademicYearSchema(BaseModel):
    year: str
    start_date: Optional[date]
    end_date: Optional[date]
    is_current: Optional[bool] = False
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None