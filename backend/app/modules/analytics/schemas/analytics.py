import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_name: str = Field(..., min_length=1, max_length=100)
    event_category: str = Field(..., min_length=1, max_length=100)
    properties: str | None = None
    user_id: uuid.UUID | None = None
    session_id: str | None = Field(None, max_length=255)


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class MetricBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric_name: str = Field(..., min_length=1, max_length=100)
    metric_value: float
    metric_type: str = Field(..., pattern="^(counter|gauge|histogram)$")
    dimensions: str | None = None
    recorded_at: str = Field(..., min_length=1, max_length=50)


class MetricCreate(MetricBase):
    pass


class MetricRead(MetricBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DashboardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=512)
    is_public: bool = False
    layout: str | None = None


class DashboardCreate(DashboardBase):
    pass


class DashboardUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=512)
    is_public: bool | None = None
    layout: str | None = None


class DashboardRead(DashboardBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
