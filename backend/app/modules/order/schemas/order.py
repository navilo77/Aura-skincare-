import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.order.schemas.billing_address import BillingAddressRead
from app.modules.order.schemas.order_item import OrderItemRead
from app.modules.order.schemas.shipping_address import ShippingAddressRead


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: uuid.UUID
    status: str = Field(
        "pending", pattern="^(pending|processing|shipped|delivered|cancelled)$"
    )
    total_amount: Decimal | None = Field(None, ge=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def currency_iso(cls, v: str) -> str:
        v = v.upper()
        if len(v) != 3:
            raise ValueError("Currency must be a 3-character ISO code")
        return v


class OrderCreate(OrderBase):
    total_amount: Decimal | None = None
    items: list[dict[str, Any]] = Field(..., min_length=1)
    shipping_address: dict[str, Any] | None = None
    billing_address: dict[str, Any] | None = None


class OrderUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(
        None, pattern="^(pending|processing|shipped|delivered|cancelled)$"
    )


class OrderRead(OrderBase):
    id: uuid.UUID
    order_number: str
    created_at: datetime
    updated_at: datetime


class OrderList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_number: str
    customer_id: uuid.UUID
    status: str
    total_amount: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime


class OrderDetail(OrderRead):
    items: list[OrderItemRead] = []
    shipping_address: ShippingAddressRead | None = None
    billing_address: BillingAddressRead | None = None
