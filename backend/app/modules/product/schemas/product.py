import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.product.schemas.brand import BrandRead
from app.modules.product.schemas.category import CategoryRead


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    brand_id: uuid.UUID
    category_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    short_description: str | None = Field(None, max_length=512)
    description: str | None = Field(None, max_length=4096)
    status: str = Field("draft", pattern="^(draft|active|archived)$")
    product_type: str = Field("simple", pattern="^(simple|variable)$")
    price: Decimal = Field(..., ge=Decimal("0"))
    compare_at_price: Decimal | None = Field(None, ge=Decimal("0"))
    currency: str = Field("USD", min_length=3, max_length=3)
    stock_quantity: int = Field(0, ge=0)
    thumbnail_url: str | None = Field(None, max_length=512)
    is_featured: bool = False
    is_active: bool = True

    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str) -> str:
        return v.lower()

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str) -> str:
        return v.upper()

    @field_validator("currency")
    @classmethod
    def currency_iso(cls, v: str) -> str:
        v = v.upper()
        if len(v) != 3:
            raise ValueError("Currency must be a 3-character ISO code")
        return v

    @field_validator("compare_at_price")
    @classmethod
    def compare_at_price_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v < 0:
            raise ValueError("compare_at_price must be greater than or equal to 0")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    brand_id: uuid.UUID | None = None
    category_id: uuid.UUID | None = None
    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255)
    sku: str | None = Field(None, min_length=1, max_length=100)
    short_description: str | None = Field(None, max_length=512)
    description: str | None = Field(None, max_length=4096)
    status: str | None = Field(None, pattern="^(draft|active|archived)$")
    product_type: str | None = Field(None, pattern="^(simple|variable)$")
    price: Decimal | None = Field(None, ge=Decimal("0"))
    compare_at_price: Decimal | None = Field(None, ge=Decimal("0"))
    currency: str | None = Field(None, min_length=3, max_length=3)
    stock_quantity: int | None = Field(None, ge=0)
    thumbnail_url: str | None = Field(None, max_length=512)
    is_featured: bool | None = None
    is_active: bool | None = None

    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.lower()
        return v

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.upper()
        return v

    @field_validator("currency")
    @classmethod
    def currency_iso(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.upper()
            if len(v) != 3:
                raise ValueError("Currency must be a 3-character ISO code")
            return v
        return v

    @field_validator("compare_at_price")
    @classmethod
    def compare_at_price_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v < 0:
            raise ValueError("compare_at_price must be greater than or equal to 0")
        return v


class ProductRead(ProductBase):
    id: uuid.UUID
    brand: BrandRead
    category: CategoryRead
    created_at: datetime
    updated_at: datetime


class ProductListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    sku: str
    price: Decimal
    currency: str
    thumbnail_url: str | None
    is_featured: bool
    is_active: bool
    brand_id: uuid.UUID
    category_id: uuid.UUID
    brand: BrandRead
    category: CategoryRead


class ProductList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    sku: str
    price: Decimal
    currency: str
    thumbnail_url: str | None = None
    is_featured: bool
    is_active: bool
    brand_id: uuid.UUID
    category_id: uuid.UUID


class ProductDetail(ProductRead):
    pass
