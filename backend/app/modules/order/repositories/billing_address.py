import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.models import BillingAddress
from app.modules.order.repositories.base import BaseRepository


class BillingAddressRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, BillingAddress)

    async def create(self, address: BillingAddress) -> BillingAddress:
        self.session.add(address)
        await self.session.flush()
        return address

    async def update(self, address: BillingAddress) -> BillingAddress:
        await self.session.merge(address)
        await self.session.flush()
        await self.session.refresh(address)
        return address

    async def get_by_id(self, address_id: uuid.UUID) -> BillingAddress | None:
        return await super().get_by_id(address_id)

    async def get_billing_address(self, order_id: uuid.UUID) -> BillingAddress | None:
        result = await self.session.execute(
            select(BillingAddress).where(BillingAddress.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        order_id: uuid.UUID | None = None,
    ) -> tuple[list[BillingAddress], int]:
        filters = []
        if order_id is not None:
            filters.append(BillingAddress.order_id == order_id)

        query = select(BillingAddress).where(*filters)
        query = query.order_by(BillingAddress.created_at.desc())

        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
