from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator


class CouponBase(BaseModel):
    code: str = Field(..., max_length=50)
    discount_type: str = Field(..., pattern="^(percentage|fixed)$")
    discount_value: Decimal = Field(..., gt=0)
    min_purchase_amount: Decimal | None = Field(None, ge=0)
    max_discount_amount: Decimal | None = Field(None, ge=0)
    usage_limit: int | None = Field(None, ge=1)
    is_active: bool = True
    starts_at: datetime
    expires_at: datetime

    @field_validator("discount_value")
    @classmethod
    def validate_discount_value(cls, value: Decimal, info: Any) -> Decimal:
        discount_type = info.data.get("discount_type")
        if discount_type == "percentage" and value > 100:
            raise ValueError("Percentage discount cannot exceed 100")
        return value


class CouponCreate(CouponBase):
    pass


class CouponUpdate(CouponBase):
    code: str | None = Field(None, max_length=50)
    discount_type: str | None = Field(None, pattern="^(percentage|fixed)$")
    discount_value: Decimal | None = Field(None, gt=0)
    starts_at: datetime | None = None
    expires_at: datetime | None = None


class CouponRead(CouponBase):
    id: uuid.UUID
    used_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
