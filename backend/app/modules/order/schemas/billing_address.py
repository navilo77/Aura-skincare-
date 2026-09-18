import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BillingAddressBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: uuid.UUID
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=20)
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=2, max_length=2)


class BillingAddressCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=20)
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=2, max_length=2)


class BillingAddressCreate(BillingAddressBase):
    pass


class BillingAddressUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str | None = Field(None, min_length=1, max_length=255)
    phone: str | None = Field(None, min_length=1, max_length=20)
    address_line1: str | None = Field(None, min_length=1, max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str | None = Field(None, min_length=1, max_length=100)
    state: str | None = Field(None, min_length=1, max_length=100)
    postal_code: str | None = Field(None, min_length=1, max_length=20)
    country: str | None = Field(None, min_length=2, max_length=2)


class BillingAddressRead(BillingAddressBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BillingAddressList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    full_name: str
    phone: str
    city: str
    state: str
    country: str
    created_at: datetime
    updated_at: datetime
