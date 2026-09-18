import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.inventory.schemas.inventory import InventoryRead


class MovementBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inventory_id: uuid.UUID
    movement_type: str = Field(
        ..., pattern="^(purchase|sale|return|transfer_in|transfer_out|adjustment)$"
    )
    quantity: int
    reference_type: str | None = Field(None, max_length=50)
    reference_id: uuid.UUID | None = None
    notes: str | None = None


class MovementCreate(MovementBase):
    pass


class MovementRead(MovementBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    inventory: InventoryRead
