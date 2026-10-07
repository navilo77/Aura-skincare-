import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.cart.models import Cart, CartItem
from app.modules.product.repositories.base import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Cart)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Cart | None:
        stmt = select(Cart).where(Cart.user_id == user_id, Cart.is_active)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID) -> Cart:
        cart = Cart(user_id=user_id, is_active=True)
        self.session.add(cart)
        await self.session.flush()
        return cart

    async def get_or_create(self, user_id: uuid.UUID) -> Cart:
        cart = await self.get_by_user_id(user_id)
        if not cart:
            cart = await self.create(user_id)
        return cart


class CartItemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CartItem)

    async def get_by_cart_and_product(
        self,
        cart_id: uuid.UUID,
        product_id: uuid.UUID,
        product_variant_id: uuid.UUID | None,
    ) -> CartItem | None:
        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
                CartItem.product_variant_id == product_variant_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_cart(self, cart_id: uuid.UUID) -> list[CartItem]:
        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def clear_by_cart(self, cart_id: uuid.UUID) -> None:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.flush()

    async def create(self, **kwargs: Any) -> CartItem:
        item = CartItem(**kwargs)
        self.session.add(item)
        await self.session.flush()
        return item

    async def update(self, item: CartItem, **kwargs: Any) -> CartItem:
        for key, value in kwargs.items():
            setattr(item, key, value)
        await self.session.flush()
        return item
