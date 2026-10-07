import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import OrderItem
from app.modules.order.repositories.order import OrderRepository
from app.modules.order.repositories.order_item import OrderItemRepository
from app.modules.product.repositories.product import ProductRepository


class OrderItemService:
    def __init__(self, session: AsyncSession):
        self.repository = OrderItemRepository(session)
        self.order_repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)

    async def create(
        self,
        order_id: uuid.UUID,
        product_id: uuid.UUID,
        quantity: int,
        unit_price: Decimal | None = None,
        variant_name: str | None = None,
    ) -> OrderItem:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status in ("delivered", "cancelled"):
            raise ValueError("Cannot modify completed orders")

        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        if not product.is_active:
            raise ValueError(f"Product {product_id} is not active")
        if product.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock for product {product_id}")

        if unit_price is None:
            unit_price = Decimal(str(product.price))

        total_price = Decimal(str(unit_price)) * Decimal(str(quantity))

        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            product_name=product.name,
            sku=product.sku,
            variant_name=variant_name,
        )
        created_item = await self.repository.create(order_item)
        await self._recalculate_order_total(order_id)
        return created_item

    async def update(
        self,
        item_id: uuid.UUID,
        quantity: int | None = None,
        unit_price: Decimal | None = None,
    ) -> OrderItem:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise ValueError("Order item not found")

        order = await self.order_repository.get_by_id(uuid.UUID(str(item.order_id)))
        if not order:
            raise ValueError("Order not found")
        if order.status in ("delivered", "cancelled"):
            raise ValueError("Cannot modify completed orders")

        if quantity is not None:
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            product = await self.product_repository.get_by_id(
                uuid.UUID(str(item.product_id))
            )
            if product and product.stock_quantity < quantity:
                raise ValueError(f"Insufficient stock for product {item.product_id}")
            item.quantity = quantity

        if unit_price is not None:
            item.unit_price = unit_price

        item.total_price = Decimal(str(float(item.unit_price))) * Decimal(
            str(item.quantity)
        )
        updated_item = await self.repository.update(item)
        await self._recalculate_order_total(uuid.UUID(str(item.order_id)))
        return updated_item

    async def delete(self, item_id: uuid.UUID) -> None:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise ValueError("Order item not found")

        order = await self.order_repository.get_by_id(uuid.UUID(str(item.order_id)))
        if not order:
            raise ValueError("Order not found")
        if order.status in ("delivered", "cancelled"):
            raise ValueError("Cannot modify completed orders")

        order_id = uuid.UUID(str(item.order_id))
        await self.repository.delete(item_id)
        await self._recalculate_order_total(order_id)

    async def _recalculate_order_total(self, order_id: uuid.UUID) -> None:
        items = await self.repository.get_all_by_order(order_id)
        total = sum((item.total_price for item in items), Decimal("0.00"))
        order = await self.order_repository.get_by_id(order_id)
        if order:
            order.total_amount = total
            await self.order_repository.update(order)

    async def get_by_id(self, item_id: uuid.UUID) -> OrderItem | None:
        return await self.repository.get_by_id(item_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        order_id: uuid.UUID | None = None,
        product_id: uuid.UUID | None = None,
    ) -> tuple[list[OrderItem], int]:
        return await self.repository.get_list(
            skip=skip, limit=limit, order_id=order_id, product_id=product_id
        )

    async def get_items_by_order(
        self, order_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[OrderItem], int]:
        return await self.repository.get_items_by_order(
            order_id, skip=skip, limit=limit
        )
