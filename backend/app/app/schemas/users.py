from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime,date

class UserCreate(BaseModel):
    user_name: str
    first_name:str
    last_name:Optional[str]=None
    age: Optional[int] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    email: str
    password: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    guardian_name: Optional[str] = None
    user_community_type: int
    roll_number: Optional[str] = None
    status: Optional[str] = 1
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class BulkUserCreate(BaseModel):
    users: List[UserCreate]
