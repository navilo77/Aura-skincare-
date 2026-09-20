import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.cart.models import Cart, CartItem
from app.modules.cart.repositories.cart import CartItemRepository, CartRepository


class CartService:
    def __init__(self, session: AsyncSession):
        self.cart_repository = CartRepository(session)
        self.item_repository = CartItemRepository(session)

    async def get_or_create_cart(self, user_id: uuid.UUID) -> Cart:
        return await self.cart_repository.get_or_create(user_id)

    async def get_cart(self, user_id: uuid.UUID) -> Cart | None:
        return await self.cart_repository.get_by_user_id(user_id)

    async def add_item(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        quantity: int,
        unit_price: Decimal,
        product_variant_id: uuid.UUID | None = None,
    ) -> CartItem:
        cart = await self.get_or_create_cart(user_id)
        existing_item = await self.item_repository.get_by_cart_and_product(
            cart.id, product_id, product_variant_id
        )
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            new_subtotal = unit_price * new_quantity
            return await self.item_repository.update(
                existing_item, quantity=new_quantity, subtotal=new_subtotal
            )
        subtotal = unit_price * quantity
        return await self.item_repository.create(
            cart_id=cart.id,
            product_id=product_id,
            product_variant_id=product_variant_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )

    async def update_item(
        self, item_id: uuid.UUID, quantity: int, unit_price: Decimal
    ) -> CartItem:
        item = await self.item_repository.get_by_id(item_id)
        if not item:
            raise ValueError("Cart item not found")
        subtotal = unit_price * quantity
        return await self.item_repository.update(
            item, quantity=quantity, subtotal=subtotal
        )

    async def remove_item(self, item_id: uuid.UUID) -> None:
        item = await self.item_repository.get_by_id(item_id)
        if not item:
            raise ValueError("Cart item not found")
        await self.item_repository.delete(item.id)

    async def get_cart_items(self, user_id: uuid.UUID) -> list[CartItem]:
        cart = await self.get_or_create_cart(user_id)
        return await self.item_repository.list_by_cart(cart.id)

    async def clear_cart(self, user_id: uuid.UUID) -> None:
        cart = await self.get_or_create_cart(user_id)
        await self.item_repository.clear_by_cart(cart.id)

    async def get_cart_summary(self, user_id: uuid.UUID) -> tuple[int, Decimal]:
        items = await self.get_cart_items(user_id)
        total_items = sum(item.quantity for item in items)
        total_amount = Decimal(str(sum(item.subtotal for item in items)))
        return total_items, total_amount
