from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookSchema(BaseModel):
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    quantity: Optional[int] = 1
    available: Optional[int] = 1
    status: Optional[str] = "available"
    created_by: Optional[int] = None
    updated_by: Optional[int] = None