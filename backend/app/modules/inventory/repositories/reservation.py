import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryReservation
from app.modules.inventory.repositories.base import BaseRepository


class InventoryReservationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, InventoryReservation)

    async def get_by_inventory(
        self, inventory_id: uuid.UUID
    ) -> list[InventoryReservation]:
        result = await self.session.execute(
            select(InventoryReservation).where(
                InventoryReservation.inventory_id == inventory_id
            )
        )
        return list(result.scalars().all())

    async def get_by_order_item(
        self, order_item_id: uuid.UUID
    ) -> InventoryReservation | None:
        result = await self.session.execute(
            select(InventoryReservation).where(
                InventoryReservation.order_item_id == order_item_id
            )
        )
        return result.scalar_one_or_none()

    async def get_active(self, inventory_id: uuid.UUID) -> list[InventoryReservation]:
        result = await self.session.execute(
            select(InventoryReservation).where(
                InventoryReservation.inventory_id == inventory_id,
                InventoryReservation.status == "reserved",
            )
        )
        return list(result.scalars().all())

    async def create(self, reservation: InventoryReservation) -> InventoryReservation:
        self.session.add(reservation)
        await self.session.flush()
        return reservation

    async def update(self, reservation: InventoryReservation) -> InventoryReservation:
        await self.session.merge(reservation)
        await self.session.flush()
        return reservation
