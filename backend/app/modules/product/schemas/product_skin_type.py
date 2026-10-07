import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductSkinTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    skin_type_id: uuid.UUID


class ProductSkinTypeCreate(ProductSkinTypeBase):
    pass


class ProductSkinTypeRead(ProductSkinTypeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
