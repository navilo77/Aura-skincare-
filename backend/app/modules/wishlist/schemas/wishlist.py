import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WishlistItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    product_variant_id: uuid.UUID | None = None


class WishlistItemRead(WishlistItemBase):
    id: uuid.UUID
    wishlist_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class WishlistBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    is_active: bool = True


class WishlistRead(WishlistBase):
    id: uuid.UUID
    items: list[WishlistItemRead] = []
    created_at: datetime
    updated_at: datetime
