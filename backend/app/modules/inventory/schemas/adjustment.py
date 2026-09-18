import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.inventory.schemas.inventory import InventoryRead


class AdjustmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inventory_id: uuid.UUID
    adjustment_type: str = Field(..., pattern="^(correction|damage|loss|found)$")
    quantity_change: int
    reason: str = Field(..., min_length=1)


class AdjustmentCreate(AdjustmentBase):
    pass


class AdjustmentRead(AdjustmentBase):
    id: uuid.UUID
    is_approved: bool
    approved_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    inventory: InventoryRead


class AdjustmentApprove(BaseModel):
    approved: bool = True
