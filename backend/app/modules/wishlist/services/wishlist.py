import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.wishlist.models import Wishlist, WishlistItem
from app.modules.wishlist.repositories.wishlist import (
    WishlistItemRepository,
    WishlistRepository,
)


class WishlistService:
    def __init__(self, session: AsyncSession):
        self.wishlist_repository = WishlistRepository(session)
        self.item_repository = WishlistItemRepository(session)

    async def get_or_create_wishlist(self, user_id: uuid.UUID) -> Wishlist:
        return await self.wishlist_repository.get_or_create(user_id)

    async def get_wishlist(self, user_id: uuid.UUID) -> Wishlist | None:
        return await self.wishlist_repository.get_by_user_id(user_id)

    async def add_item(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        product_variant_id: uuid.UUID | None = None,
    ) -> WishlistItem:
        wishlist = await self.get_or_create_wishlist(user_id)
        existing_item = await self.item_repository.get_by_wishlist_and_product(
            wishlist.id, product_id, product_variant_id
        )
        if existing_item:
            return existing_item
        return await self.item_repository.create(
            wishlist_id=wishlist.id,
            product_id=product_id,
            product_variant_id=product_variant_id,
        )

    async def remove_item(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        product_variant_id: uuid.UUID | None = None,
    ) -> None:
        wishlist = await self.get_or_create_wishlist(user_id)
        item = await self.item_repository.get_by_wishlist_and_product(
            wishlist.id, product_id, product_variant_id
        )
        if not item:
            raise ValueError("Wishlist item not found")
        await self.item_repository.delete(item.id)

    async def get_wishlist_items(self, user_id: uuid.UUID) -> list[WishlistItem]:
        wishlist = await self.get_or_create_wishlist(user_id)
        return await self.item_repository.list_by_wishlist(wishlist.id)
