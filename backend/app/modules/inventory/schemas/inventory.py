import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.inventory.schemas.warehouse import WarehouseRead


class InventoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    low_stock_threshold: int = Field(10, ge=0)
    is_tracking_enabled: bool = True


class InventoryCreate(InventoryBase):
    quantity_on_hand: int = Field(0, ge=0)
    quantity_reserved: int = Field(0, ge=0)


class InventoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    low_stock_threshold: int | None = Field(None, ge=0)
    is_tracking_enabled: bool | None = None


class InventoryRead(InventoryBase):
    id: uuid.UUID
    quantity_on_hand: int
    quantity_reserved: int
    quantity_available: int
    created_at: datetime
    updated_at: datetime
    warehouse: WarehouseRead
