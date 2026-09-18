import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WarehouseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    location: str | None = Field(None, max_length=255)
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v: str) -> str:
        return v.upper()


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=255)
    code: str | None = Field(None, min_length=1, max_length=50)
    location: str | None = Field(None, max_length=255)
    is_active: bool | None = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v: str | None) -> str | None:
        if v is not None:
            return v.upper()
        return v


class WarehouseRead(WarehouseBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
