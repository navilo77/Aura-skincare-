import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BenefitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1024)
    is_active: bool = True


class BenefitCreate(BenefitBase):
    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str) -> str:
        return v.lower()


class BenefitUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1024)
    is_active: bool | None = None

    @field_validator("slug")
    @classmethod
    def slug_lowercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.lower()
        return v


class BenefitRead(BenefitBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BenefitList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    is_active: bool
