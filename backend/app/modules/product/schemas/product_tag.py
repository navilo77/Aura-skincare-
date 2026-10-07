import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductTagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    tag_id: uuid.UUID


class ProductTagCreate(ProductTagBase):
    pass


class ProductTagRead(ProductTagBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
