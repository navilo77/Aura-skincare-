from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ActivityLogRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    description: str
    extra_metadata: str | None = Field(None, alias="metadata")
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}
