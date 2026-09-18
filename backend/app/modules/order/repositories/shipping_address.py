import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import ShippingAddress
from app.modules.order.repositories.base import BaseRepository


class ShippingAddressRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ShippingAddress)

    async def create(self, address: ShippingAddress) -> ShippingAddress:
        self.session.add(address)
        await self.session.flush()
        return address

    async def update(self, address: ShippingAddress) -> ShippingAddress:
        await self.session.merge(address)
        await self.session.flush()
        await self.session.refresh(address)
        return address

    async def get_by_id(self, address_id: uuid.UUID) -> ShippingAddress | None:
        return await super().get_by_id(address_id)

    async def get_shipping_address(self, order_id: uuid.UUID) -> ShippingAddress | None:
        result = await self.session.execute(
            select(ShippingAddress).where(ShippingAddress.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        order_id: uuid.UUID | None = None,
    ) -> tuple[list[ShippingAddress], int]:
        filters = []
        if order_id is not None:
            filters.append(ShippingAddress.order_id == order_id)

        query = select(ShippingAddress).where(*filters)
        query = query.order_by(ShippingAddress.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
