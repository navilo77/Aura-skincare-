import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    contact_email: str | None = Field(None, max_length=255)
    contact_phone: str | None = Field(None, max_length=50)
    lead_time_days: int = Field(0, ge=0)
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=255)
    contact_email: str | None = Field(None, max_length=255)
    contact_phone: str | None = Field(None, max_length=50)
    lead_time_days: int | None = Field(None, ge=0)
    is_active: bool | None = None


class SupplierRead(SupplierBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
