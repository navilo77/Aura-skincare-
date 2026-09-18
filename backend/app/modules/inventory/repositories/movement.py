import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryMovement
from app.modules.inventory.repositories.base import BaseRepository


class InventoryMovementRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InventoryMovement)

    async def get_by_inventory(
        self, inventory_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[InventoryMovement], int]:
        query = (
            select(InventoryMovement)
            .where(InventoryMovement.inventory_id == inventory_id)
            .order_by(InventoryMovement.created_at.desc())
        )
        paginated_query, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total

    async def create(self, movement: InventoryMovement) -> InventoryMovement:
        self.session.add(movement)
        await self.session.flush()
        return movement

    async def get_by_reference(
        self, reference_type: str, reference_id: uuid.UUID
    ) -> list[InventoryMovement]:
        result = await self.session.execute(
            select(InventoryMovement).where(
                InventoryMovement.reference_type == reference_type,
                InventoryMovement.reference_id == reference_id,
            )
        )
        return list(result.scalars().all())
