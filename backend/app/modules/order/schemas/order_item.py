import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=Decimal("0"))
    product_name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    variant_name: str | None = Field(None, max_length=255)


class OrderItemCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    quantity: int = Field(..., gt=0)
    variant_name: str | None = Field(None, max_length=255)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantity: int | None = Field(None, gt=0)
    unit_price: Decimal | None = Field(None, ge=Decimal("0"))


class OrderItemRead(OrderItemBase):
    id: uuid.UUID
    total_price: Decimal
    created_at: datetime
    updated_at: datetime


class OrderItemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    product_name: str
    sku: str
    variant_name: str | None = None
    created_at: datetime
    updated_at: datetime
