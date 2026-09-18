import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_id: uuid.UUID | None = Field(None)
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1024)
    image_url: str | None = Field(None, max_length=512)
    sort_order: int = Field(0, ge=0)
    is_active: bool = True


class CategoryCreate(CategoryBase):
    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str) -> str:
        return v.lower()


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_id: uuid.UUID | None = None
    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    image_url: str | None = None
    sort_order: int | None = Field(None, ge=0)
    is_active: bool | None = None

    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.lower()
        return v


class CategoryRead(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CategoryTree(CategoryRead):
    children: list["CategoryTree"] = []


CategoryTree.model_rebuild()

