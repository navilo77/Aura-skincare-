import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BrandBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1024)
    logo_url: str | None = Field(None, max_length=512)
    is_active: bool = True


class BrandCreate(BrandBase):
    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str) -> str:
        return v.lower()


class BrandUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    logo_url: str | None = None
    is_active: bool | None = None

    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.lower()
        return v


class BrandRead(BrandBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BrandList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    logo_url: str | None = None
    is_active: bool
