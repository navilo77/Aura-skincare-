import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductVariantBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., ge=Decimal("0"))
    stock_quantity: int = Field(0, ge=0)
    attributes: dict[str, Any] | None = None
    is_active: bool = True


class ProductVariantCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., ge=Decimal("0"))
    stock_quantity: int = Field(0, ge=0)
    attributes: dict[str, Any] | None = None
    is_active: bool = True

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str) -> str:
        return v.upper()


class ProductVariantCreate(ProductVariantBase):
    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str) -> str:
        return v.upper()


class ProductVariantUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID | None = None
    name: str | None = Field(None, min_length=1, max_length=255)
    sku: str | None = Field(None, min_length=1, max_length=100)
    price: Decimal | None = Field(None, ge=Decimal("0"))
    stock_quantity: int | None = Field(None, ge=0)
    attributes: dict[str, Any] | None = None
    is_active: bool | None = None

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.upper()
        return v

    @field_validator("price")
    @classmethod
    def price_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v < 0:
            raise ValueError("price must be greater than or equal to 0")
        return v


class ProductVariantRead(ProductVariantBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
