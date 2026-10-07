import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    product_variant_id: uuid.UUID | None = None
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=Decimal("0"))
    subtotal: Decimal = Field(..., ge=Decimal("0"))


class CartItemCreate(BaseModel):
    product_id: uuid.UUID
    product_variant_id: uuid.UUID | None = None
    quantity: int = Field(1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemRead(CartItemBase):
    id: uuid.UUID
    cart_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    product_name: str | None = None
    thumbnail_url: str | None = None


class CartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    is_active: bool = True


class CartRead(CartBase):
    id: uuid.UUID
    items: list[CartItemRead] = []
    created_at: datetime
    updated_at: datetime


class CartSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_items: int
    total_amount: Decimal
    currency: str = "USD"
