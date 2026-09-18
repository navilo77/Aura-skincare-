import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.inventory.schemas.supplier import SupplierRead


class ProductSupplierBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    supplier_id: uuid.UUID
    cost_price: float = Field(..., ge=0)
    is_preferred: bool = False


class ProductSupplierCreate(ProductSupplierBase):
    pass


class ProductSupplierRead(ProductSupplierBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    supplier: SupplierRead
