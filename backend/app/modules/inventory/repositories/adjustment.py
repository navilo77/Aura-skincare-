import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryAdjustment
from app.modules.inventory.repositories.base import BaseRepository


class InventoryAdjustmentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InventoryAdjustment)

    async def get_pending(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[InventoryAdjustment], int]:
        query = (
            select(InventoryAdjustment)
            .where(InventoryAdjustment.is_approved == False)  # noqa: E712
            .order_by(InventoryAdjustment.created_at.asc())
        )
        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def create(self, adjustment: InventoryAdjustment) -> InventoryAdjustment:
        self.session.add(adjustment)
        await self.session.flush()
        return adjustment

    async def update(self, adjustment: InventoryAdjustment) -> InventoryAdjustment:
        await self.session.merge(adjustment)
        await self.session.flush()
        return adjustment

    async def get_by_inventory(
        self, inventory_id: uuid.UUID
    ) -> list[InventoryAdjustment]:
        result = await self.session.execute(
            select(InventoryAdjustment).where(
                InventoryAdjustment.inventory_id == inventory_id
            )
        )
        return list(result.scalars().all())
