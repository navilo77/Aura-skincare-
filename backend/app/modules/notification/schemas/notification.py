import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TemplateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1, max_length=100)
    subject: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)
    channel: str = Field(..., pattern="^(email|sms|push|whatsapp|messenger)$")
    is_active: bool = True


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(None, min_length=1, max_length=100)
    subject: str | None = Field(None, min_length=1, max_length=255)
    body: str | None = Field(None, min_length=1)
    channel: str | None = Field(None, pattern="^(email|sms|push|whatsapp|messenger)$")
    is_active: bool | None = None


class TemplateRead(TemplateBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PreferenceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    channel: str = Field(..., pattern="^(email|sms|push|whatsapp|messenger)$")
    is_enabled: bool = True


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_enabled: bool | None = None


class PreferenceRead(PreferenceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class NotificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    template_id: uuid.UUID | None = None
    channel: str = Field(..., pattern="^(email|sms|push|whatsapp|messenger)$")
    subject: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(
        None, pattern="^(pending|sent|delivered|failed|cancelled)$"
    )
    error_message: str | None = None
    sent_at: str | None = Field(None, max_length=50)


class NotificationRead(NotificationBase):
    id: uuid.UUID
    status: str
    error_message: str | None
    sent_at: str | None
    created_at: datetime
    updated_at: datetime
