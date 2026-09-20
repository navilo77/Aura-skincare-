from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MarketingCampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    status: str
    start_date: str | None
    end_date: str | None
    created_at: datetime
    updated_at: datetime


class MarketingCampaignCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "draft"
    start_date: str | None = None
    end_date: str | None = None


class MarketingTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    content_type: str
    prompt: str
    is_active: str
    created_at: datetime
    updated_at: datetime


class MarketingTemplateCreate(BaseModel):
    name: str
    content_type: str
    prompt: str
    is_active: str = "true"


class MarketingContentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    campaign_id: uuid.UUID | None
    template_id: uuid.UUID | None
    content_type: str
    title: str | None
    body: str
    extra_metadata: str | None
    created_at: datetime
    updated_at: datetime


class MarketingContentCreate(BaseModel):
    campaign_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    content_type: str
    title: str | None = None
    body: str
    extra_metadata: str | None = None


class MarketingHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content_id: uuid.UUID | None
    action: str
    extra_metadata: str | None
    created_at: datetime
    updated_at: datetime


class MarketingAssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content_id: uuid.UUID | None
    asset_type: str
    url: str
    extra_metadata: str | None
    created_at: datetime
    updated_at: datetime


class MarketingAssetCreate(BaseModel):
    content_id: uuid.UUID | None = None
    asset_type: str
    url: str
    extra_metadata: str | None = None


class MarketingAILogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    agent: str
    prompt_version: str | None
    token_usage: int | None
    extra_metadata: str | None
    created_at: datetime
    updated_at: datetime
