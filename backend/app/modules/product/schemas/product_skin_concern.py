import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductSkinConcernBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    concern_id: uuid.UUID


class ProductSkinConcernCreate(ProductSkinConcernBase):
    pass


class ProductSkinConcernRead(ProductSkinConcernBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
