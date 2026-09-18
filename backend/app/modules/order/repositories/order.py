import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import Order
from app.modules.order.repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def create(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.flush()
        return order

    async def update(self, order: Order) -> Order:
        await self.session.merge(order)
        await self.session.flush()
        await self.session.refresh(order)
        return order

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        return await super().get_by_id(order_id)

    async def get_with_relations(self, order_id: uuid.UUID) -> Order | None:
        from sqlalchemy import select as sa_select
        from sqlalchemy.orm import selectinload

        result = await self.session.execute(
            sa_select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items),
                selectinload(Order.shipping_address),
                selectinload(Order.billing_address),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_order_number(self, order_number: str) -> Order | None:
        result = await self.session.execute(
            select(Order).where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()

    async def get_by_customer(
        self, customer_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        filters = [Order.customer_id == customer_id]

        query = select(Order).where(*filters)
        query = query.order_by(Order.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_by_status(
        self, status: str, skip: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        filters = [Order.status == status]

        query = select(Order).where(*filters)
        query = query.order_by(Order.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        customer_id: uuid.UUID | None = None,
        status: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Order], int]:
        filters = []
        if customer_id is not None:
            filters.append(Order.customer_id == customer_id)
        if status is not None:
            filters.append(Order.status == status)

        query = await self._build_query(
            *filters,
            search=search,
            search_fields=["order_number"],
        )
        query = query.order_by(Order.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
