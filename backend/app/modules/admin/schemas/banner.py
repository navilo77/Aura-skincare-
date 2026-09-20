from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class BannerBase(BaseModel):
    title: str = Field(..., max_length=255)
    subtitle: str | None = Field(None, max_length=255)
    image_url: str = Field(..., max_length=512)
    link_url: str | None = Field(None, max_length=512)
    position: str = Field(..., max_length=50)
    display_order: int = Field(0, ge=0)
    is_active: bool = True
    starts_at: datetime | None = None
    expires_at: datetime | None = None


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    title: str | None = Field(None, max_length=255)
    image_url: str | None = Field(None, max_length=512)
    position: str | None = Field(None, max_length=50)


class BannerRead(BannerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
