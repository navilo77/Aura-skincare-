import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.inventory.schemas.inventory import InventoryRead


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inventory_id: uuid.UUID
    order_item_id: uuid.UUID
    quantity: int = Field(..., gt=0)


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: uuid.UUID
    status: str
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime
    inventory: InventoryRead


class ReservationRelease(BaseModel):
    released: bool = True
