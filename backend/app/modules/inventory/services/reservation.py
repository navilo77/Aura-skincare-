import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryReservation
from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.inventory.repositories.reservation import (
    InventoryReservationRepository,
)


class ReservationService:
    def __init__(self, session: AsyncSession):
        self.repository = InventoryReservationRepository(session)
        self.inventory_repository = InventoryRepository(session)

    async def create(
        self,
        inventory_id: uuid.UUID,
        order_item_id: uuid.UUID,
        quantity: int,
    ) -> InventoryReservation:
        if quantity <= 0:
            raise ValueError("quantity must be greater than zero")

        inventory = await self.inventory_repository.get_by_id(inventory_id)
        if not inventory:
            raise ValueError("Inventory not found")

        available = inventory.quantity_on_hand - inventory.quantity_reserved
        if quantity > available:
            raise ValueError("Insufficient available stock for reservation")

        existing = await self.repository.get_by_order_item(order_item_id)
        if existing:
            raise ValueError("Reservation already exists for this order item")

        reservation = InventoryReservation(
            inventory_id=inventory_id,
            order_item_id=order_item_id,
            quantity=quantity,
            status="reserved",
        )
        return await self.repository.create(reservation)

    async def release(self, reservation_id: uuid.UUID) -> InventoryReservation:
        reservation = await self.repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reservation not found")
        if reservation.status != "reserved":
            raise ValueError("Only reserved reservations can be released")

        reservation.status = "released"
        return await self.repository.update(reservation)

    async def get_by_inventory(
        self, inventory_id: uuid.UUID
    ) -> list[InventoryReservation]:
        return await self.repository.get_by_inventory(inventory_id)

    async def get_active(self, inventory_id: uuid.UUID) -> list[InventoryReservation]:
        return await self.repository.get_active(inventory_id)
