import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = "customer"
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=255)
    is_active: bool | None = None


class UserRead(UserBase):
    id: uuid.UUID
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: uuid.UUID
    role: str
    exp: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str
