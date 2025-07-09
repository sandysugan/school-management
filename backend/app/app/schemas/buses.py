from pydantic import BaseModel
from typing import Optional, List

class BusSchema(BaseModel):
    bus_number: str
    driver_id: Optional[int] = None
    status: Optional[int] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkBusSchema(BaseModel):
    buses: List[BusSchema]
