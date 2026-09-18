import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import InventoryAdjustment
from app.modules.inventory.repositories.adjustment import InventoryAdjustmentRepository
from app.modules.inventory.repositories.inventory import InventoryRepository


class AdjustmentService:
    def __init__(self, session: AsyncSession):
        self.repository = InventoryAdjustmentRepository(session)
        self.inventory_repository = InventoryRepository(session)

    async def create(
        self,
        inventory_id: uuid.UUID,
        adjustment_type: str,
        quantity_change: int,
        reason: str,
    ) -> InventoryAdjustment:
        inventory = await self.inventory_repository.get_by_id(inventory_id)
        if not inventory:
            raise ValueError("Inventory not found")

        if quantity_change == 0:
            raise ValueError("quantity_change cannot be zero")

        adjustment = InventoryAdjustment(
            inventory_id=inventory_id,
            adjustment_type=adjustment_type,
            quantity_change=quantity_change,
            reason=reason,
        )
        return await self.repository.create(adjustment)

    async def approve(
        self,
        adjustment_id: uuid.UUID,
        approved: bool = True,
        approved_by: uuid.UUID | None = None,
    ) -> InventoryAdjustment:
        adjustment = await self.repository.get_by_id(adjustment_id)
        if not adjustment:
            raise ValueError("Adjustment not found")
        if adjustment.is_approved:
            raise ValueError("Adjustment is already approved")

        if approved and approved_by is None:
            raise ValueError("approved_by is required when approving")

        adjustment.is_approved = approved
        adjustment.approved_by = approved_by
        return await self.repository.update(adjustment)

    async def get_pending(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[InventoryAdjustment], int]:
        return await self.repository.get_pending(skip=skip, limit=limit)

    async def get_by_inventory(
        self, inventory_id: uuid.UUID
    ) -> list[InventoryAdjustment]:
        return await self.repository.get_by_inventory(inventory_id)
