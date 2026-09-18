import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=20)
    status: str = Field("active", pattern="^(active|inactive|suspended)$")
    skin_type: str | None = Field(None, max_length=50)
    skin_concerns: list[str] | None = None

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("phone")
    @classmethod
    def phone_normalize(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip()
        return v

    @field_validator("full_name")
    @classmethod
    def name_strip(cls, v: str) -> str:
        return v.strip()


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str | None = Field(None, min_length=1, max_length=255)
    email: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, max_length=20)
    status: str | None = Field(None, pattern="^(active|inactive|suspended)$")
    skin_type: str | None = Field(None, max_length=50)
    skin_concerns: list[str] | None = None

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip().lower()
        return v

    @field_validator("phone")
    @classmethod
    def phone_normalize(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip()
        return v

    @field_validator("full_name")
    @classmethod
    def name_strip(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip()
        return v


class CustomerRead(CustomerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CustomerList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    phone: str | None
    status: str
    skin_type: str | None
    created_at: datetime
    updated_at: datetime


class CustomerDetail(CustomerRead):
    pass
