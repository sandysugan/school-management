from pydantic import BaseModel
from typing import Optional, List

class DriverSchema(BaseModel):
    name: str
    license_number: str
    phone_number: Optional[str] = None
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkDriverSchema(BaseModel):
    drivers: List[DriverSchema]