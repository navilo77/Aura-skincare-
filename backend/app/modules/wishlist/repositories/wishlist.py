import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.base import BaseRepository
from app.modules.wishlist.models import Wishlist, WishlistItem


class WishlistRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wishlist)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Wishlist | None:
        stmt = select(Wishlist).where(
            Wishlist.user_id == user_id, Wishlist.is_active
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID) -> Wishlist:
        wishlist = Wishlist(user_id=user_id, is_active=True)
        self.session.add(wishlist)
        await self.session.flush()
        return wishlist

    async def get_or_create(self, user_id: uuid.UUID) -> Wishlist:
        wishlist = await self.get_by_user_id(user_id)
        if not wishlist:
            wishlist = await self.create(user_id)
        return wishlist


class WishlistItemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WishlistItem)

    async def get_by_wishlist_and_product(
        self,
        wishlist_id: uuid.UUID,
        product_id: uuid.UUID,
        product_variant_id: uuid.UUID | None,
    ) -> WishlistItem | None:
        stmt = select(WishlistItem).where(
            WishlistItem.wishlist_id == wishlist_id,
            WishlistItem.product_id == product_id,
            WishlistItem.product_variant_id == product_variant_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_wishlist(self, wishlist_id: uuid.UUID) -> list[WishlistItem]:
        stmt = select(WishlistItem).where(WishlistItem.wishlist_id == wishlist_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **kwargs: Any) -> WishlistItem:
        item = WishlistItem(**kwargs)
        self.session.add(item)
        await self.session.flush()
        return item
