import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductRoutineBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    routine_type_id: uuid.UUID


class ProductRoutineCreate(ProductRoutineBase):
    pass


class ProductRoutineRead(ProductRoutineBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
