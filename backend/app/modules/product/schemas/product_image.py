import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductImageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    image_url: str = Field(..., max_length=512)
    alt_text: str | None = Field(None, max_length=255)
    sort_order: int = Field(0, ge=0)
    is_primary: bool = False


class ProductImageCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: str = Field(..., max_length=512)
    alt_text: str | None = Field(None, max_length=255)
    sort_order: int = Field(0, ge=0)
    is_primary: bool = False


class ProductImageCreate(ProductImageBase):
    pass

    pass


class ProductImageUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: str | None = Field(None, max_length=512)
    alt_text: str | None = Field(None, max_length=255)
    sort_order: int | None = Field(None, ge=0)
    is_primary: bool | None = None


class ProductImageRead(ProductImageBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
