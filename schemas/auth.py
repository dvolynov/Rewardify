# schemas/auth.py

from pydantic import BaseModel, EmailStr, Field

import settings


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    country: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires: int = settings.auth.EXPIRES_DAYS