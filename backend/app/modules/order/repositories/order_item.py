import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import OrderItem
from app.modules.order.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderItem)

    async def create(self, item: OrderItem) -> OrderItem:
        self.session.add(item)
        await self.session.flush()
        return item

    async def update(self, item: OrderItem) -> OrderItem:
        await self.session.merge(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get_by_id(self, item_id: uuid.UUID) -> OrderItem | None:
        return await super().get_by_id(item_id)

    async def get_items_by_order(
        self, order_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[OrderItem], int]:
        filters = [OrderItem.order_id == order_id]

        query = select(OrderItem).where(*filters)
        query = query.order_by(OrderItem.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        order_id: uuid.UUID | None = None,
        product_id: uuid.UUID | None = None,
    ) -> tuple[list[OrderItem], int]:
        filters = []
        if order_id is not None:
            filters.append(OrderItem.order_id == order_id)
        if product_id is not None:
            filters.append(OrderItem.product_id == product_id)

        query = select(OrderItem).where(*filters)
        query = query.order_by(OrderItem.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_all_by_order(self, order_id: uuid.UUID) -> list[OrderItem]:
        result = await self.session.execute(
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
            .order_by(OrderItem.created_at.desc())
        )
        return list(result.scalars().all())
