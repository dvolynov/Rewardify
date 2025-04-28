# schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional


class Out(BaseModel):
    name: str
    email: EmailStr
    country: str


class Update(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    country: Optional[str] = None