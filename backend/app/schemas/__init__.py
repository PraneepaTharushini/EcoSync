from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    createdAt: datetime = Field(validation_alias="created_at")

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    token: str
    user: UserOut