import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductIngredientBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    ingredient_id: uuid.UUID


class ProductIngredientCreate(ProductIngredientBase):
    pass


class ProductIngredientRead(ProductIngredientBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
