from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class AdminSettingsRead(BaseModel):
    id: uuid.UUID
    key: str
    value: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AdminSettingsUpdate(BaseModel):
    value: str
